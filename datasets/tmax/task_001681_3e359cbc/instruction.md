You are a localization engineer managing the metrics dashboard for a global translation service. Our incoming telemetry regarding translation progress is recorded irregularly in Redis. We need a continuous hourly metrics feed that includes generated localized text summaries, served via an HTTP API. 

Your task is to fix and integrate our ETL pipeline and API service.

You have been provided with the following initial environment under `/home/user/`:
- `/home/user/seed_data.py`: A script that seeds Redis with irregular time-series data for translation events.
- `/home/user/templates/es.jinja`: A Jinja2 template for Spanish summaries.
- `/home/user/templates/fr.jinja`: A Jinja2 template for French summaries.
- `/home/user/app.py`: An incomplete Flask API skeleton.

**Step 1: Environment Setup**
1. Install necessary Python packages (e.g., `redis`, `pandas`, `flask`, `jinja2`).
2. Start a local Redis server on `127.0.0.1:6379`.
3. Run `python3 /home/user/seed_data.py` to populate the `loc_events` list in Redis.

**Step 2: DAG Orchestration & Resampling (`/home/user/pipeline.py`)**
Write a Python script at `/home/user/pipeline.py` that implements a simple sequential DAG:
1. **Extract**: Fetch all JSON records from the Redis list `loc_events`. Each record has `timestamp`, `lang`, `strings_translated`, and `missing_keys`.
2. **Transform (Resampling & Gap-Filling)**: 
   - For each language (`es`, `fr`), resample the irregular time-series data into strict hourly intervals starting from `2023-10-01T00:00:00Z` to `2023-10-02T00:00:00Z` (inclusive).
   - Use forward-filling (ffill) to fill missing hours. If the first hour is missing, back-fill it from the earliest available record.
3. **Transform (Text Generation)**: 
   - For each language and each hour, render the corresponding Jinja2 template from `/home/user/templates/`. 
   - Pass the resampled metrics (`strings_translated`, `missing_keys`) to the template to generate a `summary_text`.
4. **Load**: Save the finalized continuous data to `/home/user/processed_metrics.json` with the following structure:
   ```json
   {
     "es": {
       "2023-10-01T00:00:00Z": {"strings_translated": 10, "missing_keys": 5, "summary_text": "..."}
     },
     "fr": { ... }
   }
   ```

**Step 3: Service Integration (`/home/user/app.py`)**
Complete the Flask API in `/home/user/app.py` so it binds to `127.0.0.1:8080`. It must implement:
1. `GET /report?lang=<lang>&hour=<ISO8601>`: Reads `/home/user/processed_metrics.json` and returns the JSON dictionary for that specific language and hour. If not found, return a 404 status.
2. `POST /trigger_pipeline`: Must require the exact header `Authorization: Bearer loc-token-99`. When authorized, it executes `/home/user/pipeline.py` synchronously using `subprocess`. Upon successful execution, return a 200 OK with `{"status": "success"}`. Return 401 Unauthorized for bad tokens.

Leave the Flask app running in the background on `127.0.0.1:8080`.