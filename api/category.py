from api.base_client import BaseAPIClient

class CategoryClient(BaseAPIClient):
    URL = "https://example.com/category"

    def get_category(self, product):
        data = self.get(
            self.URL,
            params={"product": product}
        )
        if not data:
            return None
        return data["category"]