import spacy
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load actions configuration
with open("C:\\code\\AI\\workpulse.ai\\src\\actions.json", "r") as f:
    actions_config = json.load(f)

# Function to recognize intent and parameters dynamically
def recognize_intent_and_entities(transcribed_text):
    doc = nlp(transcribed_text)
    action = None
    entities = {}

    # Iterate through all actions in the configuration
    for action_name, action_data in actions_config.items():
        action_keywords = action_data["action_keywords"]
        entity_keywords = action_data["entity_keywords"]
        parameters = action_data["parameters"]

        # Check if any action keyword matches
        for token in doc:
            if token.text.lower() in action_keywords:
                action = action_name
                break

        if action:
            # Now extract entities for the recognized action
            for token in doc:
                # Check if token matches any entity keywords
                for entity in entity_keywords:
                    if entity in token.text.lower():
                        # Assuming entities are mapped to parameters, like 'repo_name' or 'repo_visibility'
                        for param in parameters:
                            if entity in param.lower():
                                entities[param] = token.text

            break

    # Return the detected action and associated entities
    if action:
        return {"intent": action, "entities": entities}
    else:
        return {"intent": "unknown", "entities": {}}
