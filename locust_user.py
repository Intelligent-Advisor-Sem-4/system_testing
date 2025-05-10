from locust import HttpUser, task, between

class UserAuthUser(HttpUser):
    # Wait time between tasks (1-3 seconds to simulate realistic user behavior)
    wait_time = between(1, 3)

    # Simulate user login to obtain JWT token
    def on_start(self):
        response = self.client.post("/auth/login", json={
            "username": "johndoe",
            "password": "123"
        })
        if response.status_code == 200:
            # Extract token (supports "token" or "access_token" keys)
            self.token = response.json().get("token") or response.json().get("access_token")
            print(f"Login successful for {self.client.base_url}")
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            self.token = None

    # Task 1: Get user profile (hypothetical, replace with actual GET endpoint)
    @task(1)
    def get_user_profile(self):
        if not self.token:
            print("Skipping task: No valid token")
            return
        response = self.client.get(
            "/auth/user/profile",  # Placeholder; replace with actual endpoint
            headers={"Authorization": f"Bearer {self.token}"},
            name="/auth/user/profile"  # Group requests in Locust stats
        )
        if response.status_code != 200:
            print(f"Get user profile failed: {response.status_code} - {response.text}")