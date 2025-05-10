from locust import HttpUser, task, between

class AdminUser(HttpUser):
    # Wait time between tasks (1-3 seconds to simulate realistic user behavior)
    wait_time = between(1, 3)

    # Simulate admin user login to obtain JWT token
    def on_start(self):
        response = self.client.post("/auth/login", json={
            "username": "johnsmith",
            "password": "admin123"
        })
        if response.status_code == 200:
            # Adjust key based on actual response format (e.g., "access_token" or "token")
            self.token = response.json()["token"] or response.json().get("access_token")
            print(f"Login successful for {self.client.base_url}")
        else:
            print(f"Login failed: {response.status_code} - {response.text}")
            self.token = None

