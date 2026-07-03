You are a data engineer building an ETL pipeline that bridges our NoSQL event store and our relational user database. We have an existing multi-service setup in `/app/` containing a MongoDB instance, a PostgreSQL instance, and a Python Flask API.

Your task is to complete the Python service (`/app/etl_service.py`) so that it properly integrates these databases and serves the aggregated analytical results over HTTP.

Currently, the Docker Compose file (`/app/docker-compose.yml`) brings up MongoDB and PostgreSQL, but the Python service is incomplete. You need to implement the `/api/v1/user-activity` endpoint in `/app/etl_service.py` to do the following:

1. Execute a NoSQL aggregation pipeline on the MongoDB `activity` database (collection `events`) to calculate the total `duration` of events per `user_id` where the `status` is "completed".
2. Load this aggregated data into the PostgreSQL database `etl_db` into a temporary table or directly join it with the existing `users` table.
3. Write a SQL query using window functions to return a JSON array of users containing: `user_id`, `username`, `department`, `total_duration`, and `department_rank`. The `department_rank` must be calculated using the `DENSE_RANK()` window function, ranking users within their specific `department` based on their `total_duration` in descending order.
4. The endpoint must accept a GET request with an optional `Authorization: Bearer etl-secret-token` header (return 401 if missing or invalid).
5. Ensure the Flask app listens on `127.0.0.1:8080`.

To complete the task:
- Edit `/app/etl_service.py` to implement the correct queries and logic.
- Start the databases using the provided docker-compose file.
- Run the Python service.

The automated verification will issue a GET request to `http://127.0.0.1:8080/api/v1/user-activity` and check the resulting JSON.