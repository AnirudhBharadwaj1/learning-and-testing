import speech_recognition as sr
import time

START_TRIGGER = "START"
STOP_TRIGGER = "END"
TERMINATE_TRIGGER = "TERMINATE"

recognizer = sr.Recognizer()

def recognize_speech(audio) -> str:
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized Speech: {text}")
        return text
    except sr.UnknownValueError:
        print("")
    except sr.RequestError as re:
        print(f"Speech recognition service error: {re}")

    return ""

def save_text(text: str) -> None:
    if text:
        with open("./output.txt", "a") as f:
            f.write(text)

def main() -> None:
    print("Listening...")
    start_time = time.time()

    with sr.Microphone() as microphone:
        recognizer.adjust_for_ambient_noise(microphone)

        comparison_text = ""
        request_flag = False
        while comparison_text != TERMINATE_TRIGGER:
            try:
                audio = recognizer.listen(microphone)
                text = recognize_speech(audio)
                comparison_text = text.upper().strip()

                # Process the words to check if any of them are keywords
                if comparison_text == START_TRIGGER:
                    request_flag = True
                    request = ""
                    print("Started capturing...")
                elif comparison_text == STOP_TRIGGER:
                    request_flag = False
                    print("Capture complete")
                    save_text(request)
                else:
                    if request_flag and text:
                        request += text
                        request += " "

            except Exception as e:
                print(f"Unexpected error: {e}")

    print(f"\nSession lasted: {time.time() - start_time} seconds")

if __name__ == "__main__":
    main()