I need your help setting up a data processing and similarity search pipeline for our ML training data.

We have a multi-service architecture running locally:
1. A Redis instance running on port 6379.
2. A Flask API running on port 5000 (currently failing to connect to Redis and missing the embedding logic).
3. An Nginx reverse proxy on port 8080 that should route traffic to the Flask API.

Your task:
1. Fix the Nginx configuration at `/home/user/nginx.conf` so that all requests to `http://localhost:8080/api/` are routed to the Flask application running on `http://localhost:5000/`. Reload or restart Nginx (running as a local user process, not systemd).
2. Fix the Flask application located at `/home/user/app/api.py`. It needs to connect to Redis using the `REDIS_HOST` and `REDIS_PORT` environment variables (or default to localhost:6379).
3. Implement the missing embedding computation in `/home/user/app/api.py`. The `/api/ingest` endpoint receives tabular data (JSON format containing `id` and `text` fields). You must convert the `text` field into a TF-IDF vector (or use a lightweight library like `scikit-learn` which is installed) and store it in Redis.
4. Implement the `/api/search` endpoint in the Flask app. It should take a `query` string, compute its embedding using the same vectorizer, and return the `id`s of the top 5 most similar texts based on cosine similarity.
5. Once the services are connected and working, write a Python script at `/home/user/ingest_data.py` that reads `/home/user/data/training_data.csv`, extracts the `id` and `description` columns, and sends them to the `http://localhost:8080/api/ingest` endpoint.
6. Run your ingest script to populate the database.

The automated test will evaluate your system by sending a set of test queries to `http://localhost:8080/api/search`. We will calculate the average Recall@5 for these queries compared to the ground truth. Your system must achieve a metric threshold of Recall@5 >= 0.85 to pass. Ensure your Flask app continues to run in the background.