You are an AI assistant helping a data scientist debug and finalize a sensor processing pipeline. 

We have a multi-service architecture located in `/home/user/pipeline/`. The system consists of:
1. An `ingress` Flask service (runs on port 8080) that receives sensor data and pushes it to a Redis queue.
2. A `redis` broker (running on a non-standard port 6380).
3. A `metrics` Flask service (runs on port 9090) that aggregates classification results.

Your objective has two parts:

**Part 1: Service Configuration**
The startup script `/home/user/pipeline/start_services.sh` brings up the three services, but they are failing to communicate. You must fix the configuration file at `/home/user/pipeline/config.yaml` so that:
- `ingress` pushes to the Redis broker at `localhost:6380`
- The `metrics_url` is correctly set to `http://localhost:9090/report`

**Part 2: The Anomaly Classifier (Adversarial Corpus)**
The pipeline relies on a missing classification script: `/home/user/pipeline/classifier.py`.
You must write this Python script. It will be used as a CLI tool to filter incoming sensor data arrays (saved as JSON arrays of floats). 

The classifier must use **density estimation and numerical integration**. Specifically, the script must:
1. Load a JSON list of floats from a file path provided as the first command-line argument.
2. Fit a Gaussian Kernel Density Estimate (KDE) to the data.
3. Numerically integrate the estimated PDF from $x = -2$ to $x = 2$.
4. If the integrated probability mass in this region is **greater than 0.05**, classify the data as an ANOMALY (reject). Otherwise, classify as NORMAL (accept).
5. Exit with status code `0` for NORMAL (accept/clean), and exit with status code `1` for ANOMALY (reject/evil).

You can test your classifier against the offline datasets provided in `/app/corpus/clean/` (which should all be accepted) and `/app/corpus/evil/` (which should all be rejected). 

Requirements:
- Write the Python code for `/home/user/pipeline/classifier.py`.
- Fix `/home/user/pipeline/config.yaml`.
- Ensure all services can communicate (you can verify by running `/home/user/pipeline/start_services.sh` and sending a test payload to `localhost:8080/data`).