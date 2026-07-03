You are a data engineer responsible for a sensor data ETL pipeline. Our pipeline ingests tabular sensor data and stores it for downstream analytics. It consists of three services:
1. **Nginx** (Reverse Proxy, meant to listen on port 8080)
2. **Flask ETL API** (Application server, running on port 5000)
3. **Redis** (Data store, running on port 6379)

We are currently facing two critical issues:

**Issue 1: Broken Pipeline Routing**
The services are provided in `/home/user/app/`. The Nginx configuration file `/home/user/app/nginx.conf` is misconfigured. When clients send POST requests to `http://127.0.0.1:8080/upload`, they are not reaching the Flask API. You must fix the Nginx configuration and ensure the `nginx`, `redis-server`, and `flask` processes are running and communicating correctly. Nginx must route `/upload` requests to the Flask app.

**Issue 2: Spoofed Sensor Data (Adversarial Ingestion)**
Malicious actors are sending spoofed sensor data to our pipeline. We have isolated samples of these files in `/home/user/data/evil/` and samples of normal, healthy sensor data in `/home/user/data/clean/`. 

We have discovered a statistical pattern to the spoofed data: the attackers artificially generate features that are perfectly or near-perfectly collinear.
You must write a standalone Python detection script at `/home/user/app/detector.py`. 
- The script must accept a single command-line argument: the absolute path to a CSV file.
- It must read the tabular data, scale the features using standardization (zero mean, unit variance), and perform dimensionality reduction (PCA).
- If the first principal component explains **more than 95% (> 0.95)** of the variance, the script must classify the file as spoofed and **exit with code 1**.
- If the first principal component explains 95% or less of the variance, the script must classify the file as clean and **exit with code 0**.

**Integration**:
Once `detector.py` is written, modify the Flask application (`/home/user/app/app.py`) so that the `/upload` endpoint saves the uploaded CSV to a temporary file, runs `/home/user/app/detector.py` on it, and:
- Returns a `400 Bad Request` if the detector exits with code 1.
- Returns a `200 OK` and saves the data to Redis (the Redis logic is already stubbed) if the detector exits with code 0.

**Verification**:
Start your services. Our automated tests will:
1. Send requests to `http://127.0.0.1:8080/upload` using the clean and evil corpora.
2. Verify that 100% of the clean corpus is accepted (200 OK).
3. Verify that 100% of the evil corpus is rejected (400 Bad Request).