import requests
from utils.logger import logger

class BaseAPIClient:
    TIMEOUT = 15

    def get(self, url, params=None):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=self.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logger.error(f"API Request Failed: {error}")
            return None