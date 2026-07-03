You are tasked with building a configuration tracking pipeline for our fleet of microservices. We have a multi-service architecture running locally that you need to glue together and extend with a data processing script.

**System Architecture (Currently Running or to be configured):**
1. **Redis Cache:** Running on `127.0.0.1:6379`.
2. **Config Stream API:** A Flask app running on port `5000`. When you send a GET request to `http://127.0.0.1:5000/stream`, it returns a large JSON array of configuration change events.
3. **Changelog Receiver:** A Flask app on port `5001`. It has a POST endpoint `http://127.0.0.1:5001/changelog` that accepts final Markdown reports.

**Your Objectives:**

1. **Reconfigure the Stream:** The Config Stream API currently has a bug where it fails to connect to Redis to cache its state. You must inspect its config at `/home/user/services/config_api/settings.env` and fix the Redis connection URL (it currently points to a wrong port/host) so the service starts returning data. Restart the service (managed by a local `systemd` user service or standard background process, you can just restart the python script `python /home/user/services/config_api/app.py &`).

2. **Data Pipeline Implementation (`/home/user/pipeline.py`):**
   Write a Python script that pulls the data from `http://127.0.0.1:5000/stream`. The data contains dictionaries with the following keys:
   `event_id` (str), `server_id` (str), `timestamp` (float), `cpu_limit` (float or null), `mem_limit` (float or null), `config_blob` (str).

   Your script must perform the following:
   * **Constraint-based Data Validation:** Discard any events where `mem_limit` is less than 512 or greater than 65536, OR `cpu_limit` is negative. (Treat `null` values as valid for this step).
   * **Interpolation and Imputation:** Sort the remaining events by `timestamp` for each `server_id`. For events where `cpu_limit` or `mem_limit` is `null`, perform linear interpolation using the closest valid values before and after it for the *same* `server_id`. If an event is at the very beginning or end and cannot be interpolated, drop it.
   * **Similarity Computation & Grouping:** For each `server_id`, compare the `config_blob` strings of adjacent events (ordered by timestamp). If two consecutive events have a Jaccard similarity of their character bigrams >= 0.8, group them together as a "Minor Tweak". Otherwise, mark it as a "Major Update".
   * **Template-based Text Generation:** For each `server_id`, generate a Markdown report summarizing the changes. The report must exactly follow this Jinja-style template format:
     ```markdown
     # Server: {server_id}
     Total valid events: {count}
     Average CPU Limit: {mean_cpu}
     Average Mem Limit: {mean_mem}
     Major Updates: {count_major}
     Minor Tweaks: {count_minor}
     ```
     (Format averages to 2 decimal places).

3. **Output and Submission:**
   * Save a JSON Lines file at `/home/user/processed_events.jsonl` containing all valid, imputed events (each line is a JSON object with `event_id, server_id, timestamp, cpu_limit, mem_limit, config_blob`).
   * Send the Markdown reports to the Changelog Receiver via POST request to `http://127.0.0.1:5001/changelog` with a JSON payload: `{"server_id": "...", "report_markdown": "..."}`.

Your data processing pipeline will be evaluated by an automated verifier that calculates the Mean Squared Error (MSE) of your imputed `cpu_limit` and `mem_limit` values against the hidden ground-truth dataset. To pass, your overall imputation MSE must be strictly less than **0.5**.