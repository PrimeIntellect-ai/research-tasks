You are a log analyst investigating multi-lingual system logs to detect anomalous mathematical access patterns. You have been given a dataset of application logs and a custom Python library to help parse and score them. However, the environment is disconnected from the internet, and the provided library contains a bug.

Your objective is to fix the library, process a stratified sample of the logs, and serve the results via an HTTP API.

Step 1: Fix the Vendored Package
There is a local package at `/app/vendored/pylogcalc-0.1.0`. It is meant to parse log messages and calculate a spatial risk score. However, it currently crashes when processing logs containing non-ASCII characters due to an incorrect encoding method. 
- Identify the bug in `/app/vendored/pylogcalc-0.1.0/pylogcalc/parser.py` (which forces `ascii` encoding) and fix it to correctly handle UTF-8 text.
- Install the package locally in your environment (e.g., `pip install -e /app/vendored/pylogcalc-0.1.0` or directly import it).

Step 2: Stratified Data Sampling
You have a log file at `/home/user/logs.jsonl` containing JSON Lines. Each line has the following keys: `{"id": int, "lang": str, "message": str, "x": float, "y": float}`.
- Parse this file.
- Perform deterministic stratified sampling: For each unique `lang` present in the dataset, extract exactly the first 5 logs (ordered by `id` ascending). Discard all other logs. 

Step 3: Data Processing and Templating
- Pass each of the sampled logs to the fixed `pylogcalc.parser.calculate_risk(log_dict)` function, which returns a float risk score.
- Sort all sampled logs globally by their calculated risk score in descending order (highest risk first). If there are ties, sort by `id` ascending.
- Take the top 3 logs with the highest risk scores.
- Using Python's `string.Template` or standard string formatting, format these top 3 logs into a JSON string exactly matching this structure:
```json
{
  "status": "success",
  "top_anomalies": [
    {"rank": 1, "id": <id>, "risk": <risk_score_rounded_to_2_decimals>},
    {"rank": 2, "id": <id>, "risk": <risk_score_rounded_to_2_decimals>},
    {"rank": 3, "id": <id>, "risk": <risk_score_rounded_to_2_decimals>}
  ]
}
```

Step 4: Expose Data via HTTP API
Write and start a Python script that runs a persistent HTTP server on `0.0.0.0` at port `9000`.
- The server must respond to `GET /api/anomalies`.
- It must return an `HTTP 200 OK` status.
- It must return the exact JSON string generated in Step 3 as the response body, with the `Content-Type: application/json` header.
- Leave this server running in the background or in a detached process so it can be queried.