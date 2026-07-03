You are a data scientist tasked with cleaning a set of sensor datasets using an automated data processing pipeline. 

There is a multi-service backend located in `/app/services/`. It consists of:
1. A Redis server (listens on port 6379) used for experiment tracking.
2. A Flask API (listens on port 5000) that provides calibration vectors.
3. An Nginx reverse proxy (listens on port 8080) that sits in front of the API.

However, the configuration is currently broken. Your tasks are as follows:

**Phase 1: Multi-Service Configuration**
1. Fix the Nginx configuration file located at `/app/services/nginx.conf`. It needs to correctly proxy requests made to `http://localhost:8080/api/` to the Flask API at `http://127.0.0.1:5000/`. 
2. Start the services using the provided `/app/services/start.sh` script. Ensure all three services are running.

**Phase 2: Data Filtering and Linear Algebra**
Write a Bash script located at `/home/user/filter.sh`. This script will act as a filter/sanitizer for sensor data files.
- The script must accept exactly one argument: the absolute path to a CSV file.
- The CSV files do not have a header and contain comma-separated numerical values representing: `sensor_id, x, y, z`.
- The script must fetch a calibration vector from the API via the Nginx proxy by making a GET request to `http://localhost:8080/api/vector`. The response will be a JSON object like `{"v_x": 0.5, "v_y": -0.5, "v_z": 1.0}`.
- For each row in the CSV, your script must compute the dot product of the sensor vector `[x, y, z]` and the calibration vector `[v_x, v_y, v_z]`.
- **Filtering Logic**: If the absolute value of the dot product for *any* row in the CSV file is strictly greater than `10.000` (evaluating numerical accuracy), the entire file is considered "anomalous" (evil). Otherwise, it is "clean".
- **Experiment Tracking**: 
  - If the file is anomalous, your script must use `redis-cli` to add the base name of the file to a Redis set called `rejected_files`, and the script must exit with status code `1`.
  - If the file is clean, add the base name of the file to a Redis set called `accepted_files`, and exit with status code `0`.

**Testing Requirements**
Your script `/home/user/filter.sh` must be executable (`chmod +x`).
We will run an automated verifier that passes files from two corpora to your script:
- `/app/corpus/clean/`: Contains clean CSV files. Your script must exit 0 for all of these.
- `/app/corpus/evil/`: Contains anomalous CSV files. Your script must exit 1 for all of these.

You may use standard Linux tools (e.g., bash, awk, jq, curl, redis-cli, python3) inside your script.