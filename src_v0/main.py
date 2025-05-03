import os
from speech_to_text import convert_speech_to_text
from intent_recognition import recognize_intent_and_entities
from ask_for_input import ask_for_missing_input, ask_for_valid_input, extract_details
from mcp_server import create_repository
from utils import speak
import time

def main():
    speak("Hi sir, how can i help you...")  # Initial prompt
    
    while True:  # Keep listening for the user's voice continuously
        # Step 1: Get audio input from the user
        transcribed_text = convert_speech_to_text()
        print(f"Recognized Text: {transcribed_text}")
        
        if transcribed_text:
            # Step 2: Recognize intent
            intent_entities = recognize_intent_and_entities(transcribed_text)
            print(f"Detected Intent: {intent_entities}")
        
            # Step 3: Handle additional input if needed
            prompts = ask_for_missing_input(intent_entities, extract_details(transcribed_text, intent_entities["intent"]))


            if intent_entities["intent"] == "create_repository":
                # Assuming user gave the repository name
                repo_name = None
                repo_description = None
                repo_visibility = None
                for prompt in prompts:
                    # check for prompts and ask for valid input
                    speak(prompt)
                    user_response = convert_speech_to_text()  # Get the response after each prompt
                    print(f"User Response: {user_response}")

                    # Store the responses based on the prompt
                    if "name" in prompt.lower():
                        repo_name = ask_for_valid_input(prompt, validation_function=lambda x: len(x.strip()) > 0)
                    elif "description" in prompt.lower():
                        repo_description = ask_for_valid_input(prompt, validation_function=lambda x: len(x.strip()) > 0)
                    elif "public" in prompt.lower() or "private" in prompt.lower():
                        repo_visibility = ask_for_valid_input(prompt, validation_function=lambda x: x.strip().lower() in ["public", "private"])

                # Step 5: Create the repository with the collected details
                if repo_name :
                    create_repository(repo_name, repo_description, repo_visibility)

            # elif intent["intent"] == "create_issue":
            #     # Implement issue creation logic here
            #     issue_title = "Sample Issue"
            #     issue_description = "This is a sample issue created by voice."
            #     create_issue(issue_title, issue_description)
                
            # Step 4: Ask the user if they want to continue or exit
            print("What would you like to do next?")
            
        else:
            print("Sorry, I couldn't hear you clearly. Please try again.")
        
        # Add a small delay to avoid rapid looping and overwhelming the system
        time.sleep(1)

if __name__ == "__main__":
    main()
