from core.stt import listen
from core.llm_client import detect_intent_and_params
from core.conversation import fill_missing_params
from mcp_caller import call_tool

def main():
    while True:
        text = listen()
        if not text:
            continue

        intent_data = detect_intent_and_params(text)
        print(f"🎯 Detected Intent: {intent_data['intent']}")
        print(f"📦 Extracted Parameters: {intent_data['parameters']}")

        if intent_data["missing_parameters"]:
            print("⚠️ Some parameters are missing, asking...")
            completed_data = fill_missing_params(intent_data)
        else:
            completed_data = intent_data

        result = call_tool(completed_data)
        print(f"✅ Result: {result}")

if __name__ == "__main__":
    main()
