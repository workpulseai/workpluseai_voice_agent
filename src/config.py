import os
from dotenv import load_dotenv

load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = "gpt-3.5-turbo"  # or any other model
