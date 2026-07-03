You are an MLOps engineer responsible for maintaining a local experiment tracking system and ensuring the integrity of the tabular data artifacts (training logs) uploaded by researchers. 

Currently, our local tracking stack is broken, and malicious/corrupted training logs are poisoning our downstream visualization dashboards.

Your task has two main parts:

### Part 1: Service Composition & Configuration
We have a local pipeline consisting of Nginx (as a reverse proxy) and a Flask artifact tracking server. 
1. The Flask app is located at `/app/tracking_server.py`. It runs on port `5000`.
2. The Nginx configuration file is at `/etc/nginx/sites-available/default`. You must configure it so that it proxies incoming requests on port `8080` to the Flask app on `127.0.0.1:5000`.
3. The Flask app relies on an environment variable `VALIDATOR_SCRIPT`. You must create a startup script at `/home/user/start_pipeline.sh` that starts Nginx, sets `VALIDATOR_SCRIPT=/home/user/validator.py`, and starts the Flask application in the background.

### Part 2: Data Validation Classifier
Researchers upload their training logs (CSV files) to the tracking server. Before saving, the Flask app will execute your script: 
`python3 $VALIDATOR_SCRIPT <path_to_csv>`

You must write this script (`/home/user/validator.py`) to act as an anomaly detector and schema validator. The script must inspect the CSV file and:
- Exit with code `0` if the file is a **clean**, valid training log.
- Exit with code `1` if the file is **anomalous**, corrupted, or maliciously formatted.

To be considered a "clean" training log, the CSV MUST adhere strictly to these rules:
- It must contain exactly these headers: `epoch`, `loss`, `accuracy`.
- `epoch` must be parsable as a non-negative integer.
- `loss` must be a positive float (> 0.0).
- `accuracy` must be a float between 0.0 and 1.0 inclusive.
- There must be no missing values (NaNs/empty cells) in any column.

Corrupted ("evil") files might contain negative losses, out-of-bounds accuracies, missing columns, trailing commas, or strings injected into numeric columns.

Write the code, fix the configuration, and ensure your `start_pipeline.sh` script leaves the services running perfectly so that an automated end-to-end upload test will succeed.