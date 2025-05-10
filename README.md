# Locust Performance Tests for Intelligent Advisor API

This directory contains Locust test scripts for performance testing the API endpoints of the "Intelligent Advisor for Personal Finance & Investment" system. Each script targets a specific API section: admin, predictions, user, budget, profile, and assets. This README explains how to run the tests and store the results.

## Prerequisites

1. **Python 3.10+**: Ensure Python is installed.
   ```bash
   python --version
   ```
2. **Locust**: Install Locust using pip.
   ```bash
   pip install locust
   ```
3. **Environment Setup**:
   - Clone the repository or copy the `tests/locust` directory.
   - Update test credentials and parameters in each script (e.g., `test_user`, `test_pass`, user IDs, tickers).
   - Ensure access to the staging API (`https://api-intellifinance.shancloudservice.com`).
4. **Dependencies**: Each script assumes FastAPI, SQLAlchemy, and other dependencies are handled server-side. No additional client-side dependencies are needed beyond Locust.

## Directory Structure

The Locust scripts are located in the `tests/locust` directory:

```
tests/locust/
├── locust_admin.py        # Tests admin section GET endpoints
├── locust_predictions.py  # Tests predictions section GET endpoints
├── locust_user.py         # Tests user section GET endpoints
├── locust_budget.py       # Tests budget section GET endpoints
├── locust_profile.py      # Tests profile section GET endpoints
├── locust_assets.py       # Tests assets section GET endpoints
```

Each script is self-contained and tests all GET endpoints for its respective API section.

## Updating Test Parameters

Before running tests, update the following in each script:
- **Credentials**: Replace `test_user` and `test_pass` in the `on_start` method with valid staging credentials.
  ```python
  response = self.client.post("/auth/login", json={
      "username": "test_user",  # Replace with valid username
      "password": "test_pass"   # Replace with valid password
  })
  ```
- **Parameters**: Update user IDs, tickers, or other parameters (e.g., `user_ids`, `tickers`, `screener_types`) with valid values from the staging database.
  - Example for `locust_assets.py`:
    ```python
    tickers = ["AAPL", "GOOGL", "MSFT", "AMZN"]  # Replace with valid tickers
    screener_types = ["growth", "value", "dividend", "tech"]  # Replace with ScreenerType enum values
    ```
  - Query the database or API to get valid values:
    ```bash
    curl https://api-intellifinance.shancloudservice.com/assets/screener-types  # For screener types
    ```
- Verify credentials:
  ```bash
  curl -X POST https://api-intellifinance.shancloudservice.com/auth/login -H "Content-Type: application/json" -d '{"username":"test_user","password":"test_pass"}'
  ```

## Running Tests

Tests can be run in two modes:
- **Web Mode**: Interactive UI for configuring and monitoring tests.
- **Headless Mode**: Automated runs with CSV output for scripting or CI.

### Web Mode
Run Locust with the web interface to configure users, spawn rate, and monitor results in real-time.

1. **Command Template**:
   ```bash
   locust -f <script_name> --host=https://api-intellifinance.shancloudservice.com
   ```
   Replace `<script_name>` with the script file (e.g., `locust_admin.py`).

2. **Section-Specific Commands**:
   - **Admin**:
     ```bash
     locust -f tests/locust/locust_admin.py --host=https://api-intellifinance.shancloudservice.com
     ```
   - **Predictions**:
     ```bash
     locust -f tests/locust/locust_predictions.py --host=https://api-intellifinance.shancloudservice.com
     ```
   - **User**:
     ```bash
     locust -f tests/locust/locust_user.py --host=https://api-intellifinance.shancloudservice.com
     ```
   - **Budget**:
     ```bash
     locust -f tests/locust/locust_budget.py --host=https://api-intellifinance.shancloudservice.com
     ```
   - **Profile**:
     ```bash
     locust -f tests/locust/locust_profile.py --host=https://api-intellifinance.shancloudservice.com
     ```
   - **Assets**:
     ```bash
     locust -f tests/locust/locust_assets.py --host=https://api-intellifinance.shancloudservice.com
     ```

3. **Access the UI**:
   - Open `http://localhost:8089` in a browser (or the testing machine’s IP if remote).
   - Configure:
     - **Number of users**: 10 (recommended for initial load testing).
     - **Spawn rate**: 1 user/second.
     - **Host**: `https://api-intellifinance.shancloudservice.com` (pre-filled from command).
   - Start the test and monitor response times, error rates, and RPS.

### Headless Mode
Run Locust without the UI for automated testing, saving results to CSV files.

1. **Command Template**:
   ```bash
   locust -f <script_name> --host=https://api-intellifinance.shancloudservice.com --users=10 --spawn-rate=1 --run-time=10m --headless --csv=<output_prefix>
   ```
   - `<script_name>`: Script file (e.g., `locust_admin.py`).
   - `<output_prefix>`: Prefix for CSV output files (e.g., `admin_test_results`).
   - `--users=10`: Simulates 10 concurrent users.
   - `--spawn-rate=1`: Spawns 1 user per second.
   - `--run-time=10m`: Runs for 10 minutes.

2. **Section-Specific Commands**:
   - **Admin**:
     ```bash
     locust -f tests/locust/locust_admin.py --host=https://api-intellifinance.shancloudservice.com --users=10 --spawn-rate=1 --run-time=10m --headless --csv=admin_test_results
     ```
   - **Predictions**:
     ```bash
     locust -f tests/locust/locust_predictions.py --host=https://api-intellifinance.shancloudservice.com --users=10 --spawn-rate=1 --run-time=10m --headless --csv=predictions_test_results
     ```
   - **User**:
     ```bash
     locust -f tests/locust/locust_user.py --host=https://api-intellifinance.shancloudservice.com --users=10 --spawn-rate=1 --run-time=10m --headless --csv=user_test_results
     ```
   - **Budget**:
     ```bash
     locust -f tests/locust/locust_budget.py --host=https://api-intellifinance.shancloudservice.com --users=10 --spawn-rate=1 --run-time=10m --headless --csv=budget_test_results
     ```
   - **Profile**:
     ```bash
     locust -f tests/locust/locust_profile.py --host=https://api-intellifinance.shancloudservice.com --users=10 --spawn-rate=1 --run-time=10m --headless --csv=profile_test_results
     ```
   - **Assets**:
     ```bash
     locust -f tests/locust/locust_assets.py --host=https://api-intellifinance.shancloudservice.com --users=10 --spawn-rate=1 --run-time=10m --headless --csv=assets_test_results
     ```

3. **Notes**:
   - Adjust `--users`, `--spawn-rate`, and `--run-time` based on testing needs (e.g., `--users=100` for stress testing, `--run-time=8h` for soak testing).
   - Ensure rate limits (e.g., 100 requests/minute for general API, 10 requests/minute for `/auth/login`) are respected to avoid HTTP 429/503 errors.

## Storing and Interpreting Results

### Saving Results
In headless mode, Locust generates CSV files with the `--csv` flag. For each test, two files are created:
- **`<output_prefix>_stats.csv`**: Aggregated statistics (e.g., response times, request rates, error rates).
- **`<output_prefix>_stats_history.csv`**: Time-series data for response times and other metrics.

Example for `locust_admin.py`:
```bash
locust -f tests/locust/locust_admin.py --host=https://api-intellifinance.shancloudservice.com --users=10 --spawn-rate=1 --run-time=10m --headless --csv=admin_test_results
```
Output files:
- `admin_test_results_stats.csv`
- `admin_test_results_stats_history.csv`

### File Structure
- **Stats CSV**:
  - Columns: `Type`, `Name`, `Request Count`, `Failure Count`, `Median Response Time`, `Average Response Time`, `Min Response Time`, `Max Response Time`, `Average Content Size`, `Requests/s`, `Failures/s`, `50%`, `66%`, `75%`, `80%`, `90%`, `95%`, `99%`, `99.9%`, `99.99%`, `100%`.
  - Example:
    ```
    Type,Name,Request Count,Failure Count,Median Response Time,...
    GET,/admin/endpoint,100,2,200,...
    ```
  - Use to verify KPIs (e.g., p95 response time < 500ms, error rate < 0.1%, per Section 7.2).
- **Stats History CSV**:
  - Columns: `Timestamp`, `User Count`, `Type`, `Name`, `Request Count`, `Failure Count`, `Median Response Time`, ...
  - Example:
    ```
    Timestamp,User Count,Type,Name,Request Count,...
    1698765432,10,GET,/admin/endpoint,50,...
    ```
  - Use for time-series analysis (e.g., plot response times over time).

### Storing Results
1. **Local Storage**:
   - CSV files are saved in the directory where the Locust command is run.
   - Organize results in a subdirectory (e.g., `tests/results`):
     ```bash
     mkdir -p tests/results
     mv *_test_results*.csv tests/results/
     ```
2. **Archiving**:
   - Compress results for long-term storage:
     ```bash
     tar -czf tests/results/archive_$(date +%Y%m%d).tar.gz tests/results/*.csv
     ```
3. **Cloud Storage**:
   - Upload to a cloud service (e.g., AWS S3) for team access:
     ```bash
     aws s3 cp tests/results/ s3://your-bucket/locust-results/ --recursive
     ```
4. **Version Control** (Optional):
   - Store results in a Git repository (ensure sensitive data is excluded):
     ```bash
     git add tests/results/*.csv
     git commit -m "Add Locust test results for 2025-05-11"
     git push
     ```

### Interpreting Results
- **Key Metrics**:
  - **p95 Response Time**: Should be < 500ms (Section 7.2). Check the `95%` column in `_stats.csv`.
  - **Error Rate**: Should be < 0.1% (Section 7.2). Calculate as `Failure Count / Request Count`.
  - **Requests/s**: Ensure throughput meets expected load.
- **Visualization**:
  - Use tools like Excel, Pandas, or Grafana to visualize `_stats_history.csv`:
    ```python
    import pandas as pd
    df = pd.read_csv("admin_test_results_stats_history.csv")
    df.plot(x="Timestamp", y="Median Response Time", title="Response Time Over Time")
    ```
  - Import CSVs into Grafana for dashboards (requires CSV data source plugin).
- **Validation**:
  - Compare metrics against performance KPIs (Section 7.2).
  - Investigate high failure rates or slow response times using FastAPI logs:
    ```logql
    {job="fastapi"} |= "ERROR"
    ```

## Combining Tests
To test all sections simultaneously:
1. **Single Locust File**:
   - Create a combined script importing all user classes:
     ```python
     from locust_admin import AdminUser
     from locust_predictions import PredictionsUser
     from locust_user import UserAuthUser
     from locust_budget import BudgetUser
     from locust_profile import ProfileUser
     from locust_assets import AssetsUser
     ```
   - Save as `locust_combined.py` and run:
     ```bash
     locust -f tests/locust/locust_combined.py --host=https://api-intellifinance.shancloudservice.com
     ```
2. **Multiple Instances**:
   - Run each script as a separate Locust instance (master-worker setup):
     ```bash
     locust -f tests/locust/locust_admin.py --host=https://api-intellifinance.shancloudservice.com --master &
     locust -f tests/locust/locust_predictions.py --host=https://api-intellifinance.shancloudservice.com --worker &
     locust -f tests/locust/locust_user.py --host=https://api-intellifinance.shancloudservice.com --worker &
     locust -f tests/locust/locust_budget.py --host=https://api-intellifinance.shancloudservice.com --worker &
     locust -f tests/locust/locust_profile.py --host=https://api-intellifinance.shancloudservice.com --worker &
     locust -f tests/locust/locust_assets.py --host=https://api-intellifinance.shancloudservice.com --worker &
     ```
   - Access the master UI at `http://localhost:8089` to control workers.

## Troubleshooting
1. **Login Failures**:
   - **Symptom**: Console shows “Login failed: 404” or “Login failed: 500”.
   - **Solution**:
     - Verify credentials:
       ```bash
       curl -X POST https://api-intellifinance.shancloudservice.com/auth/login -H "Content-Type: application/json" -d '{"username":"test_user","password":"test_pass"}'
       ```
     - Ensure `test_user` exists in the database.
     - Check FastAPI logs:
       ```bash
       journalctl -u fastapi.service
       ```
2. **HTTP 404 Errors**:
   - **Symptom**: Endpoints return 404 (e.g., invalid ticker, user ID).
   - **Solution**:
     - Update parameters (e.g., `user_ids`, `tickers`) with valid values:
       ```sql
       SELECT id FROM users;  # For user IDs
       SELECT ticker_symbol FROM stocks;  # For tickers
       ```
     - Check FastAPI logs:
       ```logql
       {job="fastapi"} |= "not found"
       ```
3. **HTTP 401/403 Errors**:
   - **Symptom**: Authentication errors for endpoints.
   - **Solution**:
     - Ensure valid token in script. Test authentication:
       ```bash
       curl -H "Authorization: Bearer <token>" https://api-intellifinance.shancloudservice.com/<endpoint>
       ```
     - If endpoint is unauthenticated, remove `headers` from the task.
4. **HTTP 429/503 Errors**:
   - **Symptom**: Rate limiting or service unavailable.
   - **Solution**:
     - Reduce `--users` (e.g., `--users=5`).
     - Check Nginx rate limits (Section 6.4):
       ```bash
       sudo cat /etc/nginx/nginx.conf
       ```
     - Monitor logs:
       ```logql
       {job="nginx"} |= "429"
       ```
5. **HTTP 500 Errors**:
   - **Symptom**: Server or database errors.
   - **Solution**:
     - Check database connectivity (AWS RDS, Section 9.2):
       ```logql
       {job="postgresql"} |= "ERROR"
       ```
     - Verify FastAPI logs:
       ```logql
       {job="fastapi"} |= "ERROR"
       ```
