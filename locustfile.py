from locust import HttpUser, task, between
from utils.config_reader import ConfigReader

class GreenGrocerUser(HttpUser):
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks

    def on_start(self):
        config = ConfigReader()
        self.client.base_url = config.get_base_url()

    @task(3)
    def view_homepage(self):
        self.client.get("/")

    @task(2)
    def search_products(self):
        self.client.get("/api/products", params={"q": "organic"})

    @task(1)
    def view_product(self):
        self.client.get("/api/products/1")  # Assuming product with ID 1 exists
