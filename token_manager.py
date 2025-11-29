import os
import json
from datetime import datetime, timedelta

class TokenManager:
    def __init__(self, token_file='tokens.json'):
        self.token_file = token_file
        self.tokens = self._load_tokens()

    def _load_tokens(self):
        """Load tokens from a JSON file (simulating a simple DB or file-based storage)."""
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as file:
                return json.load(file)
        return {}

    def _save_tokens(self):
        """Save tokens to the JSON file."""
        with open(self.token_file, 'w') as file:
            json.dump(self.tokens, file)

    def get_token(self, service_name):
        """Retrieve the token for a specific service."""
        token_info = self.tokens.get(service_name)
        if token_info and self._is_token_valid(token_info['expires_at']):
            return token_info['access_token']
        return None

    def set_token(self, service_name, access_token, expires_in):
        """Set a new token for a service and save it."""
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        self.tokens[service_name] = {
            'access_token': access_token,
            'expires_at': expires_at.isoformat()
        }
        self._save_tokens()

    def refresh_token(self, service_name, new_access_token, expires_in):
        """Refresh the access token for a service."""
        self.set_token(service_name, new_access_token, expires_in)

    def _is_token_valid(self, expires_at_str):
        """Check if the token is still valid."""
        expires_at = datetime.fromisoformat(expires_at_str)
        return expires_at > datetime.now()