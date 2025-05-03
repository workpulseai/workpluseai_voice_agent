import pyttsx3

def initialize_engine_with_female_voice():
    """Initializes the pyttsx3 engine with a female voice."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Set the voice to female (index 1 is usually female)
    engine.setProperty('voice', voices[1].id)
    return engine

engine = initialize_engine_with_female_voice()


def speak(text):
    """Converts text to speech using the given engine."""
    engine.say(text)
    engine.runAndWait()

# Example usage
