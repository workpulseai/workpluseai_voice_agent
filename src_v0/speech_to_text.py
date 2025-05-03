import speech_recognition as sr


def convert_speech_to_text():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the system's microphone as the audio source
    with sr.Microphone() as source:
        print("Say something...")
        
        # Adjust for ambient noise and listen to the user's speech
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            # Use Google Web Speech API to convert the speech to text
            print("Recognizing...")
            transcribed_text = recognizer.recognize_google(audio)
            return transcribed_text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return ""
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            return ""