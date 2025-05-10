from locust import HttpUser, task, between
import random

class ProfileUser(HttpUser):
    # Wait time between tasks (1-3 seconds to simulate realistic user behavior)
    wait_time = between(1, 3)

    # Sample user IDs for testing
    user_ids = ["19aaa01d-4413-467c-82ee-2f30defb2fee", "123e4567-e89b-12d3-a456-426614174000"]

    # Simulate user login to obtain JWT token
    def on_start(self):
        response = self.client.post("/auth/login", json={
            "username": "test_user",
            "password": "test_pass"
        })
        if response.status_code == 200:
            # Extract token (supports "token" or "access_token" keys)
            self.token = response.json().get("token") or response.json().get("access_token")
            print(f"Login successful for {self.client.base_url}")
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            self.token = None

    # Task 1: Ping endpoint (unauthenticated)
    @task(1)
    def ping(self):
        response = self.client.get(
            "/profile/ping",
            name="/profile/ping"
        )
        if response.status_code != 200:
            print(f"Ping failed: {response.status_code} - {response.text}")

    # Task 2: Get portfolio tickers
    @task(2)
    def get_portfolio(self):
        if not self.token:
            print("Skipping task: No valid token")
            return
        response = self.client.get(
            "/profile/get_portfolio",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/profile/get_portfolio"
        )
        if response.status_code != 200:
            print(f"Get portfolio failed: {response.status_code} - {response.text}")

    # Task 3: Get risk score
    @task(2)
    def get_risk_score(self):
        if not self.token:
            print("Skipping task: No valid token")
            return
        user_id = random.choice(self.user_ids)
        response = self.client.get(
            f"/profile/risk_score?user_id={user_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/profile/risk_score"
        )
        if response.status_code not in (200, 204):
            print(f"Get risk score failed: {response.status_code} - {response.text}")