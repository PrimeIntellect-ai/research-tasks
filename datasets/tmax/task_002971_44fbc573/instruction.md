You are tasked with fixing a broken internal user management system, extracting user data from a legacy dump, and migrating the accounts into the new system with strict performance requirements. 

Here is the situation:
1. **Broken Infrastructure**: There is a pre-packaged user management API located at `/app/vendored_usermgmt`. It is a Docker Compose application consisting of a Python FastAPI service and a PostgreSQL database. Currently, the services cannot reach each other due to network misconfigurations and incorrect environment variables in the provided files. Your first task is to debug and fix the files in `/app/vendored_usermgmt` so that `docker compose up -d` successfully starts the API on `http://localhost:8000` and the API can talk to the database.

2. **Health Monitoring**: Create a shell script at `/home/user/health_monitor.sh` that checks the API health endpoint (`http://localhost:8000/health`) every 2 seconds. If it returns HTTP 200, it should append `[OK] $(date +%s)` to `/home/user/api_health.log`. If it fails, append `[FAIL] $(date +%s)`. Run this in the background once the API is fixed.

3. **Legacy Data Processing**: You have a messy system log file at `/home/user/legacy_users.txt` containing 10,000 lines. Mixed within debug logs are user records formatted exactly like:
   `[USER-MIGRATE] username: <username> | email: <email> | role: <role>`
   Use command-line text processing tools (awk, sed, grep) to extract only these valid user records into a clean CSV file at `/home/user/clean_users.csv` with the headers `username,email,role`.

4. **High-Performance Migration Script**: Write a Python script at `/home/user/import_users.py` that reads `/home/user/clean_users.csv` and POSTs each user to the API at `http://localhost:8000/users` (JSON payload: `{"username": "...", "email": "...", "role": "..."}`). 
   *Crucial Performance Requirement*: The API has a simulated internal latency of 15ms per request. If you send requests synchronously, importing 5,000 users will take over 75 seconds. You MUST implement your Python script using asynchronous I/O (e.g., `asyncio` and `aiohttp`) or a thread pool to import all users concurrently. 

To pass, your script `/home/user/import_users.py` must successfully import all users into the database, and its total execution time for 5,000 extracted users must be **under 12.0 seconds**.