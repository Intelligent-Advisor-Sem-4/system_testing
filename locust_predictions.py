from locust import HttpUser, task, between

class PredictionsUser(HttpUser):
    # Wait time between tasks (1-3 seconds to simulate realistic user behavior)
    wait_time = between(1, 3)

    # Simulate user login to obtain JWT token (optional, included for consistency)
    def on_start(self):
        response = self.client.post("/auth/login", json={
            "username": "johndoe",
            "password": "123"
        })
        if response.status_code == 200:
            # Support both "token" and "access_token" response formats
            self.token = response.json().get("token") or response.json().get("access_token")
            print(f"Login successful for {self.client.base_url}")
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            self.token = None

    # Task 1: Get active stock symbols
    @task(1)
    def get_active_symbols(self):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        response = self.client.get(
            "/get-active-symbols",
            headers=headers,
            name="/get-active-symbols"  # Group requests in Locust stats
        )
        if response.status_code != 200:
            print(f"Get active symbols failed: {response.status_code} - {response.text}")