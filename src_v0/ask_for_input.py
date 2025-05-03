from utils import  speak
from speech_to_text import convert_speech_to_text

import re

# Function to extract relevant details from user input
def extract_details(text, action_type):
    details = {}

    if action_type == "create_repository":
        # Extract repo name, description, and visibility
        name_match = re.search(r"repo name[s]? (\w+)", text, re.IGNORECASE)
        if name_match:
            details['name'] = name_match.group(1)
        
        description_match = re.search(r"description (.+)", text, re.IGNORECASE)
        if description_match:
            details['description'] = description_match.group(1)
        
        visibility_match = re.search(r"(public|private)", text, re.IGNORECASE)
        if visibility_match:
            details['visibility'] = visibility_match.group(1).lower()

    elif action_type == "create_issue":
        # Extract issue title and description
        title_match = re.search(r"issue title (.+)", text, re.IGNORECASE)
        if title_match:
            details['title'] = title_match.group(1)
        
        description_match = re.search(r"description (.+)", text, re.IGNORECASE)
        if description_match:
            details['description'] = description_match.group(1)
    
    # Add more action types and extraction logic here...

    return details

def ask_for_missing_input(action_type, collected_data):
    """Dynamically ask for missing data based on action type and already collected info."""
    prompts = []

    if action_type == "create_repository":
        if 'name' not in collected_data:
            prompts.append("What should be the name of the repository?")
        if 'description' not in collected_data:
            prompts.append("What is the description of the repository?")
        if 'visibility' not in collected_data:
            prompts.append("Should the repository be public or private?")

    elif action_type == "create_issue":
        if 'title' not in collected_data:
            prompts.append("What is the title of the issue?")
        if 'description' not in collected_data:
            prompts.append("What is the description of the issue?")
    
    # Add more cases here for other action types

    return prompts


def ask_for_valid_input(prompt, validation_function=None, retry_message="I didn't understand that. Can you please repeat?"):
    """Ask for input until a valid response is received."""
    while True:
        speak(prompt)
        user_response = convert_speech_to_text()  # Get the response from the user
        print(f"User Response: {user_response}")
        
        if user_response.strip():  # Check if the response is not empty
            if validation_function and not validation_function(user_response):
                speak(retry_message)  # Let the user know the input is invalid
                print("Invalid input, asking again.")
            else:
                return user_response  # Valid response
        else:
            speak(retry_message)
            print("Invalid input, asking again.")