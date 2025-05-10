from locust import HttpUser, task, between
import random

class BudgetUser(HttpUser):
    # Wait time between tasks (1-3 seconds to simulate realistic user behavior)
    wait_time = between(1, 3)

    # Sample user IDs and transaction data for testing
    user_ids = ["19aaa01d-4413-467c-82ee-2f30defb2fee", "123e4567-e89b-12d3-a456-426614174000"]
    transaction_descriptions = [
        "Grocery shopping at Walmart",
        "Coffee at Starbucks",
        "Monthly rent payment",
        "Gym membership"
    ]
    transaction_types = ["expense", "income"]

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

    # Task 1: Get financial predictions
    @task(3)
    def get_predictions(self):
        if not self.token:
            print("Skipping task: No valid token")
            return
        user_id = random.choice(self.user_ids)
        response = self.client.get(
            f"/budget/predictions?user_id={user_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/budget/predictions"
        )
        if response.status_code != 200:
            print(f"Get predictions failed: {response.status_code} - {response.text}")

    # Task 2: Get budget report
    @task(2)
    def get_budget_report(self):
        if not self.token:
            print("Skipping task: No valid token")
            return
        user_id = random.choice(self.user_ids)
        response = self.client.get(
            f"/budget/budget-report?user_id={user_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/budget/budget-report"
        )
        if response.status_code != 200:
            print(f"Get budget report failed: {response.status_code} - {response.text}")

    # Task 3: Categorize transaction
    @task(2)
    def categorize_transaction(self):
        description = random.choice(self.transaction_descriptions)
        amount = round(random.uniform(5.0, 500.0), 2)
        type_ = random.choice(self.transaction_types)
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        response = self.client.get(
            f"/budget/categorize-transaction?description={description}&amount={amount}&type={type_}",
            headers=headers,
            name="/budget/categorize-transaction"
        )
        if response.status_code != 200:
            print(f"Categorize transaction failed: {response.status_code} - {response.text}")

    # Task 4: Chat with LLM
    @task(1)
    def chat(self):
        prompts = [
            "How can I save more on groceries?",
            "What’s the best way to budget for travel?",
            "Should I invest my savings?"
        ]
        prompt = random.choice(prompts)
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        response = self.client.get(
            f"/budget/chat?prompt={prompt}",
            headers=headers,
            name="/budget/chat"
        )
        if response.status_code != 200:
            print(f"Chat failed: {response.status_code} - {response.text}")

    # Task 5: Send budget report email
    @task(1)
    def send_email(self):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        response = self.client.get(
            "/budget/email",
            headers=headers,
            name="/budget/email"
        )
        if response.status_code != 200:
            print(f"Send email failed: {response.status_code} - {response.text}")

    # Task 6: Get user transactions
    @task(2)
    def get_transactions(self):
        if not self.token:
            print("Skipping task: No valid token")
            return
        user_id = random.choice(self.user_ids)
        response = self.client.get(
            f"/budget/transactions/{user_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/budget/transactions"
        )
        if response.status_code != 200:
            print(f"Get transactions failed: {response.status_code} - {response.text}")

    # Task 7: Get transactions by category
    @task(1)
    def get_transactions_by_category(self):
        if not self.token:
            print("Skipping task: No valid token")
            return
        user_id = random.choice(self.user_ids)
        response = self.client.get(
            f"/budget/transactions/categories/{user_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/budget/transactions/categories"
        )
        if response.status_code != 200:
            print(f"Get transactions by category failed: {response.status_code} - {response.text}")

    # Task 8: Get transaction summary
    @task(2)
    def get_transaction_summary(self):
        if not self.token:
            print("Skipping task: No valid token")
            return
        user_id = random.choice(self.user_ids)
        response = self.client.get(
            f"/budget/transactions/summary/{user_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/budget/transactions/summary"
        )
        if response.status_code != 200:
            print(f"Get transaction summary failed: {response.status_code} - {response.text}")

    # Task 9: Get budget goals
    @task(2)
    def get_budget_goals(self):
        if not self.token:
            print("Skipping task: No valid token")
            return
        user_id = random.choice(self.user_ids)
        response = self.client.get(
            f"/budget/budget-goals/{user_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/budget/budget-goals"
        )
        if response.status_code != 200:
            print(f"Get budget goals failed: {response.status_code} - {response.text}")