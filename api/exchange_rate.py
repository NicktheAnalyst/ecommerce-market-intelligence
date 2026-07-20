from api.base_client import BaseAPIClient

class ExchangeRateClient(BaseAPIClient):
    URL = "https://open.er-api.com/v6/latest/USD"

    def get_rates(self):
        data = self.get(self.URL)
        if not data:
            return {}
        return data["rates"]