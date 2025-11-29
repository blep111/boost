# token_manager.py

import json
import os

TOKEN_FILE = 'tokens.json'

# Load tokens from file (if it exists)
def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

# Save tokens to file
def save_tokens(tokens):
    with open(TOKEN_FILE, 'w') as file:
        json.dump(tokens, file, indent=4)

# Add a new token
def add_token(token_name, token_value):
    tokens = load_tokens()
    tokens[token_name] = token_value
    save_tokens(tokens)

# Get the access token for a user
def get_token(token_name):
    tokens = load_tokens()
    return tokens.get(token_name)