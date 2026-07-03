I need you to build a log processing pipeline for our new microservice architecture. We have three services running: an Nginx reverse proxy, a Flask API, and a Redis cache. 

Currently, these services are not properly configured to trace requests end-to-end, and we need to analyze performance bottlenecks.

Here is what you need to do:
1. **Service Configuration**:
   - The services are defined in `/home/user/app/docker-compose.yml`. 
   - Modify the Nginx configuration (`/home/user/app/nginx/nginx.conf`) to include a custom header `X-Request-Id` (a unique UUID) for every incoming request and pass it to the upstream Flask app. Log this ID in the Nginx access logs.
   - Modify the Flask app (`/home/user/app/flask/app.py`) to extract this `X-Request-Id`, log it in its JSON-formatted application logs, and use it as a key prefix when querying Redis.
   - Start the services using Docker Compose.

2. **Traffic Generation**:
   - Run the provided script `/home/user/app/generate_traffic.sh` which will send a burst of requests to the Nginx endpoint (http://localhost:8080).

3. **Data Processing Pipeline**:
   - Write a Python script at `/home/user/pipeline.py` that processes the generated Nginx NCSA extended logs, the Flask JSON logs, and the Redis keyspace events.
   - You must use Regex to parse the Nginx logs.
   - Join Nginx access data (timestamp, URL, status code, latency) with Flask application logs (internal processing steps, DB query times) using the `X-Request-Id`.
   - Identify "anomalous" requests. A request is anomalous if Nginx reports a 5xx status code OR if the total Nginx latency is more than 2x the internal Flask processing time (indicating queueing or network issues).
   - Write the final joined dataset of anomalous requests to `/home/user/anomalies.parquet` using the Parquet format. The Parquet file must have the following schema: `request_id` (string), `timestamp` (string), `url` (string), `status_code` (int), `nginx_latency` (float), `flask_latency` (float), `anomaly_reason` (string).

Your script must be highly accurate in identifying these anomalies compared to our baseline dataset.