from api.base_client import BaseAPIClient

class ShippingClient(BaseAPIClient):
    URL = "https://example.com/shipping"

    def get_shipping_cost(self, country):
        data = self.get(
            self.URL,
            params={"country": country}
        )
        if not data:
            return None
        return data["shipping_cost"]