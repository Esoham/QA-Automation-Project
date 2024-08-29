from .base_api import BaseAPI

class ProductAPI(BaseAPI):
    def get_product(self, product_id):
        return self.get(f"/api/products/{product_id}")

    def search_products(self, query):
        return self.get("/api/products", params={"q": query})

    def create_product(self, product_data):
        return self.post("/api/products", json=product_data)

    def update_product(self, product_id, product_data):
        return self.put(f"/api/products/{product_id}", json=product_data)

    def delete_product(self, product_id):
        return self.delete(f"/api/products/{product_id}")
