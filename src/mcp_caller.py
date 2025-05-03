import requests
from config import MCP_SERVER_URL
from tools.github import prepare_create_repo_payload

def call_tool(intent_data):
    intent = intent_data["intent"]
    params = intent_data["parameters"]

    if intent == "create_repository":
        payload = prepare_create_repo_payload(params)
    else:
        return "🚫 Unknown intent."

    response = requests.post(MCP_SERVER_URL, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed with status {response.status_code}: {response.text}"
