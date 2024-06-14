import requests
import time
import base64
import json
from api_aguas_interface.logger_config import logger  # Import the logger from the logger_config module

class Access:
    def __init__(self, endpoint, username, password):
        if username is '' or password is '':
            raise ValueError("Username or password cannot be None")
        self.token_endpoint = endpoint + "token/"
        self.refresh_endpoint = endpoint + "token/refresh/"
        try:
            self._get_initial_tokens(username, password)
            logger.info("Access class initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Access class: {e}")
            raise

    def _get_initial_tokens(self, username, password):
        payload = {"username": username, "password": password}
        try:
            response = requests.post(self.token_endpoint, json=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            self.data = response.json()
            self.access_token = self.data['access']
            self.refresh_token = self.data['refresh']
            self.token_expiry = self._get_token_expiry(self.access_token)
            logger.debug(f"Initial tokens received: {self.data}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse token response: {e}")
            raise

    def _get_token_expiry(self, token):
        try:
            payload = token.split('.')[1]
            padding = '=' * (4 - len(payload) % 4)
            decoded_payload = base64.urlsafe_b64decode(payload + padding)
            exp_time = json.loads(decoded_payload)['exp']
            logger.debug(f"Token expiry time: {exp_time}")
            return exp_time
        except (IndexError, ValueError, KeyError, json.JSONDecodeError) as e:
            logger.error(f"Failed to decode token expiry: {e}")
            raise

    def _refresh_token(self):
        payload = {"refresh": self.refresh_token}
        try:
            response = requests.post(self.refresh_endpoint, json=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            new_tokens = response.json()
            self.access_token = new_tokens['access']
            self.token_expiry = self._get_token_expiry(self.access_token)
            logger.info("Token refreshed")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse refresh token response: {e}")
            raise

    def __call__(self):
        current_time = time.time()
        minutes_to_expiry = (self.token_expiry - current_time) / 60
        logger.info(f"Token will expire in {minutes_to_expiry:.2f} minutes.")

        if current_time >= self.token_expiry:
            try:
                self._refresh_token()
                logger.info("Token refreshed automatically.")
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")
                raise

        return self.access_token