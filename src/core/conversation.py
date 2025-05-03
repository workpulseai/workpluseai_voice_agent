from core.stt import listen

def fill_missing_params(intent_data):
    parameters = intent_data["parameters"]
    missing = intent_data["missing_parameters"]

    for param in missing:
        print(f"❓ Please specify {param}: ")
        response = listen()
        parameters[param] = response

    return {
        "intent": intent_data["intent"],
        "parameters": parameters
    }
