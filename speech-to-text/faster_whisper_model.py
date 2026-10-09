# Before running:
# Execute following to download faster-whisper-base:
# from huggingface_hub import snapshot_download
# snapshot_download("Systran/faster-whisper-base", local_dir="./models/faster-whisper-base")

import queue
import re
import time
from collections import deque

import numpy as np
import pyaudio
from faster_whisper import WhisperModel

# CONSTANTS
MODEL = "./models/faster-whisper-base"
LANGUAGE = "en"
COMPUTE_TYPE = "int8"
DEVICE = "cpu"

RATE = 16_000              # Whisper expects 16 kHz mono
CHUNK = 1024               # ~64 ms per chunk
INPUT_DEVICE = None        # None = default mic; or an int index (see list_devices())

SILENCE_SECONDS = 0.8      # pause length that ends a phrase
MAX_PHRASE_SECONDS = 25    # force a flush on very long speech
PREROLL_CHUNKS = 5         # keep ~0.3 s before speech starts so first word isn't clipped
MIN_PHRASE_SECONDS = 0.4   # ignore tiny blips (clicks, coughs)

SHOW_PARTIALS = True       # live partial text (only shown while capturing)
PARTIAL_INTERVAL = 1.5

START_TRIGGER = "START"
STOP_TRIGGER = "STOP"
TERMINATE_TRIGGER = "TERMINATE"

# Matches any trigger as a WHOLE word, case-insensitive ("send"/"friend" won't match "end")
TRIGGER_RE = re.compile(
    r"\b(" + "|".join(re.escape(t) for t in (START_TRIGGER, STOP_TRIGGER, TERMINATE_TRIGGER)) + r")\b",
    re.IGNORECASE,
)

def rms(chunk: bytes) -> float:
    """
    Use root mean square to get noise level from the chunks
    Handles conversion to float32 to prevent overflow and handles divide by zero
    """
    samples = np.frombuffer(chunk, dtype=np.int16).astype(np.float32)
    return float(np.sqrt(np.mean(samples**2))) if samples.size else 0.0

def to_float32(frames: list[bytes]) -> np.ndarray:
    """
    PyAudio gives int16 but processing for faster-whisper requires float32, so convert
    """
    pcm = np.frombuffer(b"".join(frames), dtype=np.int16)
    return pcm.astype(np.float32) / 32768.0

def transcribe(model: WhisperModel, audio: np.ndarray, fast: bool = False) -> str:
    """
    Get lazy generator using the model.transcribe function and then parse text from the segment objects
    """
    segments, _ = model.transcribe(
        audio,
        language=LANGUAGE,
        beam_size=1 if fast else 5,
        vad_filter=True,                      # drops silence -> fewer hallucinations
        vad_parameters={"min_silence_duration_ms": 500},
        condition_on_previous_text=False,
    )
    return "".join(s.text for s in segments).strip()

def calibrate(q: "queue.Queue[bytes]", seconds: float = 1.0) -> float:
    """Measure room noise and pick a speech threshold above it."""
    print("Calibrating background noise (stay quiet)...")
    levels = []
    end = time.time() + seconds
    while time.time() < end:
        try:
            levels.append(rms(q.get(timeout=0.5)))
        except queue.Empty:
            pass
    ambient = float(np.mean(levels)) if levels else 100.0
    threshold = max(ambient * 3.0, 300.0)
    print(f"Ambient level {ambient:.0f} -> speech threshold {threshold:.0f}")
    return threshold

def emit(text: str) -> None:
    """Print captured text, trimming punctuation left over from the trigger words."""
    text = text.lstrip(" ,.;:!?-").rstrip(" ,;:-")
    if text:
        print(f">> {text}")

def process_phrase(text: str, capturing: bool) -> tuple[bool, bool]:
    """Walk through a transcribed phrase, honouring trigger words in order.

    Returns (capturing, terminate). Text is only printed while capturing is True,
    so "start hello world end" prints "hello world", and a phrase with no triggers
    is ignored unless we were already capturing.
    """
    pos = 0
    for m in TRIGGER_RE.finditer(text):
        if capturing:
            emit(text[pos:m.start()])          # text spoken before this trigger
        pos = m.end()
        word = m.group(1).upper()

        if word == START_TRIGGER and not capturing:
            capturing = True
            print("[capture started]")
        elif word == STOP_TRIGGER and capturing:
            capturing = False
            print("[capture stopped]")
        elif word == TERMINATE_TRIGGER:
            return capturing, True

    if capturing:
        emit(text[pos:])                       # text after the last trigger
    return capturing, False

def main() -> None:
    print("Loading Whisper model...")
    model = WhisperModel(MODEL, device=DEVICE, compute_type=COMPUTE_TYPE)
    print("Model loaded.")

    pa = pyaudio.PyAudio()
    q: "queue.Queue[bytes]" = queue.Queue()

    def callback(in_data, frame_count, time_info, status):
        """
        Gets called by pyaudio when audio is captured and stores hte audio bytes in the queue
        First part of tuple indicates what the output strema should do and the second says what hte input stream should do
        """
        q.put(in_data)
        return (None, pyaudio.paContinue)

    # Creates audio stream
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        input_device_index=INPUT_DEVICE,
        frames_per_buffer=CHUNK,
        stream_callback=callback,
    )

    max_silent = int(SILENCE_SECONDS * RATE / CHUNK)
    max_chunks = int(MAX_PHRASE_SECONDS * RATE / CHUNK)
    min_chunks = int(MIN_PHRASE_SECONDS * RATE / CHUNK)

    try:
        threshold = calibrate(q)
        print("\nListening...\n")

        preroll: deque[bytes] = deque(maxlen=PREROLL_CHUNKS)
        frames: list[bytes] = []
        speaking = False
        capturing = False          # True between START and END
        silent = 0
        last_partial = 0.0
        last_partial_len = 0

        def flush() -> bool:
            """Transcribe the finished phrase and apply triggers. Returns True to terminate."""
            nonlocal frames, speaking, silent, last_partial_len, capturing
            terminate = False

            if len(frames) - silent >= min_chunks:
                text = transcribe(model, to_float32(frames))
                if SHOW_PARTIALS:
                    print("\r" + " " * 100 + "\r", end="")  # clear partial line
                if text:
                    capturing, terminate = process_phrase(text, capturing)
            elif SHOW_PARTIALS:
                print("\r" + " " * 100 + "\r", end="")

            frames, speaking, silent, last_partial_len = [], False, 0, 0
            return terminate

        while True:
            try:
                chunk = q.get(timeout=0.5)
            except queue.Empty:
                continue

            if rms(chunk) > threshold:
                if not speaking:
                    speaking = True
                    frames = list(preroll)
                    last_partial = time.time()
                frames.append(chunk)
                silent = 0
            elif speaking:
                frames.append(chunk)
                silent += 1
            else:
                preroll.append(chunk)
                continue

            # End of phrase: long enough pause, or phrase got too long
            if speaking and (silent >= max_silent or len(frames) >= max_chunks):
                if flush():
                    print("[terminated]")
                    break
                continue

            # Live partial transcript - only while capturing, so nothing is shown
            # (or even transcribed) before you say the start trigger
            if (
                SHOW_PARTIALS
                and capturing
                and speaking
                and time.time() - last_partial >= PARTIAL_INTERVAL
                and len(frames) > last_partial_len
            ):
                partial = transcribe(model, to_float32(frames), fast=True)
                last_partial = time.time()
                last_partial_len = len(frames)
                if partial:
                    print("\r" + (partial + " ...")[:99].ljust(99), end="", flush=True)

    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

if __name__ == "__main__":
    main()