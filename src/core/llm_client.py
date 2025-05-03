from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Hugging Face API key from environment variable
HF_API_KEY = os.getenv("HF_API_KEY")

print("Hugging Face API Key:", HF_API_KEY)
# Check if the token is loaded correctly
if not HF_API_KEY:
    raise ValueError("HF_API_KEY is not set in the environment variables")

# Load the tokenizer and model using the authentication token
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token=HF_API_KEY)
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", use_auth_token=HF_API_KEY)

def detect_intent_and_params(text):
    # Define your prompt
    prompt = prompt = f"""
You are an intent recognition assistant for GitHub actions.

You must:
- Identify which intent from the list below matches the user's input.
- Extract the parameters required for that intent.
- If any parameters are missing or unclear, include them in "missing_parameters".

INTENT LIST:

1 **create_or_update_file**
- Inputs: owner (string), repo (string), path (string), content (string), message (string), branch (string), sha (optional string)

2 **push_files**
- Inputs: owner (string), repo (string), branch (string), files (array of {{ path, content }}), message (string)

3 **search_repositories**
- Inputs: query (string), page (optional number), perPage (optional number)

4 **create_repository**
- Inputs: name (string), description (optional string), private (optional boolean), autoInit (optional boolean)

5 **get_file_contents**
- Inputs: owner (string), repo (string), path (string), branch (optional string)

6 **create_issue**
- Inputs: owner (string), repo (string), title (string), body (optional string), assignees (optional string[]), labels (optional string[]), milestone (optional number)

7 **create_pull_request**
- Inputs: owner (string), repo (string), title (string), body (optional string), head (string), base (string), draft (optional boolean), maintainer_can_modify (optional boolean)

8 **fork_repository**
- Inputs: owner (string), repo (string), organization (optional string)

9 **create_branch**
- Inputs: owner (string), repo (string), branch (string), from_branch (optional string)

10 **list_issues**
- Inputs: owner (string), repo (string), state (optional string), labels (optional string[]), sort (optional string), direction (optional string), since (optional string), page (optional number), per_page (optional number)

11 **update_issue**
- Inputs: owner (string), repo (string), issue_number (number), title (optional string), body (optional string), state (optional string), labels (optional string[]), assignees (optional string[]), milestone (optional number)

12 **add_issue_comment**
- Inputs: owner (string), repo (string), issue_number (number), body (string)

13 **search_code**
- Inputs: q (string), sort (optional string), order (optional string), per_page (optional number), page (optional number)

14 **search_issues**
- Inputs: q (string), sort (optional string), order (optional string), per_page (optional number), page (optional number)

15 **search_users**
- Inputs: q (string), sort (optional string), order (optional string), per_page (optional number), page (optional number)

16 **list_commits**
- Inputs: owner (string), repo (string), page (optional string), per_page (optional string), sha (optional string)

17 **get_issue**
- Inputs: owner (string), repo (string), issue_number (number)

18 **get_pull_request**
- Inputs: owner (string), repo (string), pull_number (number)

19 **list_pull_requests**
- Inputs: owner (string), repo (string), state (optional string), head (optional string), base (optional string), sort (optional string), direction (optional string), per_page (optional number), page (optional number)

20 **create_pull_request_review**
- Inputs: owner (string), repo (string), pull_number (number), body (string), event (string: 'APPROVE', 'REQUEST_CHANGES', 'COMMENT'), commit_id (optional string), comments (optional array of {{ path, position, body }})

21 **merge_pull_request**
- Inputs: owner (string), repo (string), pull_number (number), commit_title (optional string), commit_message (optional string), merge_method (optional string: 'merge', 'squash', 'rebase')

22 **get_pull_request_files**
- Inputs: owner (string), repo (string), pull_number (number)

23 **get_pull_request_status**
- Inputs: owner (string), repo (string), pull_number (number)

24 **update_pull_request_branch**
- Inputs: owner (string), repo (string), pull_number (number), expected_head_sha (optional string)

25 **get_pull_request_comments**
- Inputs: owner (string), repo (string), pull_number (number)

26 **get_pull_request_reviews**
- Inputs: owner (string), repo (string), pull_number (number)

---

EXAMPLE RESPONSE FORMAT:

{{
  "intent": "create_repository",
  "parameters": {{
    "name": "my-new-repo",
    "description": "A demo repo",
    "private": true,
    "autoInit": true
  }},
  "missing_parameters": []
}}

Input: "{text}"

Your response:
"""

    # Tokenize the input prompt
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate response using the LLaMA model
    outputs = model.generate(
        **inputs,
        max_length=2000,  # Adjust based on the expected response length
        num_beams=5,  # You can fine-tune this value
        temperature=0.7,  # Control the randomness of the output
        no_repeat_ngram_size=2  # Prevent repetition of phrases
    )

    # Decode the output and extract the JSON part
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Print the full result (for debugging purposes)
    print("Result:", result)

    # Parse and return the result (assuming it's a valid JSON)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {"intent": "unknown", "entities": {}}
