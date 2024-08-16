import string
import time
import random

from locust import HttpUser, task, between

def generate_random_login(length=25):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_login = ''.join(random.choice(characters) for _ in range(length))
    return random_login

class QuickstartUser(HttpUser):
    wait_time = between(0, 2)

    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)

    def on_start(self):
        login = generate_random_login()
        self.client.post("/reg", json={
            "login": str(login),
            "password": "string"
        })
