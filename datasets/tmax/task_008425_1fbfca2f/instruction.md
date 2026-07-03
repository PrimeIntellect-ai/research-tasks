You are a QA Engineer setting up a test environment and executing a security test suite for a new Go-based financial microservice. The service is currently failing to compile, lacks a database, and needs to be tested for concurrency vulnerabilities. 

Your task consists of the following phases:

**Phase 1: Fix the Go Build (Circular Import)**
The source code for the service is located in `/home/user/service/`. Currently, running `go build` fails due to a circular import between the `account` and `auth` packages. 
1. Analyze the Go source code in `/home/user/service/`.
2. Refactor the code to resolve the circular import without changing the core business logic or HTTP endpoint signatures.
3. Successfully compile the Go service into an executable named `server` inside `/home/user/service/`.

**Phase 2: Schema Migration & Dependencies (Python)**
The service requires a SQLite database to run.
1. Create a Python virtual environment at `/home/user/venv`.
2. Install the `requests` library in this virtual environment.
3. Write a Python script at `/home/user/migrate.py` that reads the SQL file located at `/home/user/schema.sql` and executes it against a new SQLite database at `/home/user/service/db.sqlite3`.
4. Run your migration script so the database is correctly seeded.

**Phase 3: Web Security Concurrency Test (Python)**
The service has an endpoint `POST /redeem` that accepts JSON `{"username": "<name>", "code": "<coupon_code>"}`. The developers implemented this using standard Go HTTP handlers (which spawn goroutines), but you suspect a Time-of-Check to Time-of-Use (TOCTOU) race condition exists when redeeming a coupon.
1. Start the compiled Go `server` in the background. It will listen on `http://127.0.0.1:8080`.
2. Write a Python script at `/home/user/exploit.py` (using your venv) that creates a new user via `POST /register` (payload: `{"username": "qa_tester"}`). 
3. The script must then use Python concurrency (e.g., `concurrent.futures.ThreadPoolExecutor`) to send 20 simultaneous requests to `POST /redeem` for the user `qa_tester` using the coupon code `WELCOME50`. (This coupon should normally only add $50 once).
4. Finally, the script should fetch the user's balance via `GET /balance?username=qa_tester` and write *only* the integer balance to `/home/user/report.txt`.

Ensure the final balance in `/home/user/report.txt` reflects the result of the race condition exploit (it should be > 50 if the exploit is successful).