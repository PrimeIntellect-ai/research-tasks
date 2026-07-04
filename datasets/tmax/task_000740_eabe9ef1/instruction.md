You are a data analyst tasked with building a data sanitization pipeline for a machine learning project. We discovered that our training datasets contain leaked samples from our test set, as well as some poisoned records. 

We have a local Bayesian scoring service designed to detect these anomalies. However, the microservice stack for this scoring system is currently broken. Your job is to fix the services and write a Bash script that processes our raw CSV files, joins them with a large-scale local storage reference, and filters out the bad data.

### Step 1: Fix the Microservices
The scoring system consists of three services:
1. **Redis**: Running on port `6379`. Contains pre-computed word probabilities and embedding cluster references.
2. **Scoring API (Flask)**: Located in `/app/api/`. It is supposed to run on port `5000` but is failing to connect to Redis. Check its environment/configuration files.
3. **Nginx**: Acts as a reverse proxy on port `8080`. It is currently misconfigured and returning 502 Bad Gateway when trying to reach the Scoring API.

You must identify the misconfigurations in `/app/api/.env` and `/etc/nginx/conf.d/api.conf`, correct them, and ensure the API is running and reachable via `http://localhost:8080/score`. 
*Note: You may need to start or restart the services (Nginx and the Flask app) using standard Linux commands.*

### Step 2: Write the Data Processing Script
Create a Bash script at `/home/user/pipeline.sh` that takes two arguments: an input CSV file and an output CSV file.
```bash
/home/user/pipeline.sh <input_csv_path> <output_csv_path>
```

**Input CSV Format:**
```csv
id,text_data
101,this is a sample row
102,suspicious data point
```

**Reference CSV (`/app/data/embeddings.csv`):**
```csv
id,cluster_id
101,c_44
102,c_99
```

**Requirements for `pipeline.sh`:**
1. Using pure Bash tools (e.g., `join`, `awk`, `sed`), join the input CSV with `/app/data/embeddings.csv` on the `id` column. Both files are sorted by `id`.
2. For each data row (skipping the header), query the scoring API via `curl`:
   `GET http://localhost:8080/score?cluster=<cluster_id>&text=<text_data>`
   (Make sure to URL-encode the parameters, or use `curl -G --data-urlencode`).
3. The API returns a JSON response: `{"status": "clean"}` or `{"status": "evil"}`.
4. If the status is `"clean"`, write the original input row (just `id,text_data`) to the output CSV. If it is `"evil"`, drop the row.
5. The output CSV must include the original header (`id,text_data`).

You must ensure your script correctly handles all rows and perfectly preserves clean data while dropping all flagged data.