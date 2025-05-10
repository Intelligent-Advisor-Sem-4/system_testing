from locust import HttpUser, task, between

class FinanceUser(HttpUser):
    # Wait time between tasks (1-3 seconds to simulate realistic user behavior)
    wait_time = between(1, 3)

    # Simulate user login to obtain JWT token
    def on_start(self):
        response = self.client.post("/auth/login", json={
            "username": "johndoe",
            "password": "123"
        })
        if response.status_code == 200:
            self.token = response.json()["token"]
        else:
            print("Login failed:", response.status_code)

    # Task 1: Stock Prediction (Group 37)
    @task(3)  # Weight: 3 (more frequent)
    def predict_stock(self):
        self.client.get(
            "/stocks/predict?ticker=AAPL",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    # Task 2: Add Budget Entry (Group 38)
    @task(2)
    def add_budget(self):
        self.client.post(
            "/budget/add",
            json={"amount": 100.50, "category": "Food", "date": "2025-05-10"},
            headers={"Authorization": f"Bearer {self.token}"}
        )

    # Task 3: Portfolio Optimization (Group 39)
    @task(1)
    def optimize_portfolio(self):
        self.client.post(
            "/portfolio/optimize",
            json={"assets": ["AAPL", "GOOGL"], "investment_amount": 10000},
            headers={"Authorization": f"Bearer {self.token}"}
        )

    # Task 4: Risk Assessment (Group 40)
    @task(1)
    def assess_risk(self):
        self.client.get(
            "/risk/assess?portfolio_id=123",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    # Task 5: Health Check
    @task(1)
    def health_check(self):
        self.client.get("/health")