import requests
import os
from dotenv import load_dotenv

load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")

def create_repository(name, description, visibility):
    url = f"{MCP_SERVER_URL}"
    data = {
        "action": "create_repository",
        "name": name,
    }
    if description:
        data["description"] = description
    if visibility:
        data["visibility"] = visibility.lower()
    print(f"url: {url}")
    print(f"data: {data}")
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Successfully created repository: {response.json()}")
    else:
        print(f"Response: {response.json()}")
        print(f"Failed to create repository: {response.status_code}")
