You are a log analyst investigating anomalous traffic patterns from our global servers. We have an influx of multi-language log data and need a real-time detection service to identify changepoints in error rates. 

Your task is to build and run a Python-based HTTP service that ingests logs, joins them with metadata, processes unicode text, and serves anomaly detection results.

Here are your instructions:

1. **Extract Configuration:**
   You have been provided an image at `/app/incident_report.png`. Use OCR to read this image. It contains critical handwritten configuration details, specifically a "PORT" and an anomaly "Z_THRESHOLD". 

2. **Build the HTTP Service:**
   Create a Python web service (e.g., using Flask or FastAPI) that listens on `127.0.0.1` at the PORT extracted from the image.
   
   The service must expose two endpoints:
   
   **A. `POST /ingest`**
   - Accepts a JSON payload containing a list of log entries: `[{"timestamp": "YYYY-MM-DDTHH:MM:SS", "ip": "192.168.1.x", "message": "..."}]`
   - **Text Processing**: For each log, analyze the `message` string. If the number of non-ASCII (Unicode) characters is strictly greater than the number of ASCII characters, tag the log as `is_intl = true`, otherwise `false`.
   - **Data Join**: Join the log entry with the metadata found in `/app/meta.csv` (which has columns `ip,region`). If an IP is missing from the CSV, default region to `UNKNOWN`.
   - Store these processed records in memory or a local database. Return HTTP 200.

   **B. `GET /anomalies`**
   - When called, the service must aggregate the stored logs into 1-minute time windows per `region`.
   - **Parallel/Pipeline logic**: Calculate the total number of `is_intl = true` logs per minute per region.
   - **Anomaly Detection**: For each region's time-series, calculate the mean ($\mu$) and standard deviation ($\sigma$) of the `intl` log counts across all available 1-minute windows. A window is an anomaly if its count is greater than $\mu + (Z\_THRESHOLD \times \sigma)$. (If $\sigma$ is 0, no anomalies should be flagged).
   - Return a JSON response mapping regions to their anomalous timestamps:
     ```json
     {
       "region_name": ["YYYY-MM-DDTHH:MM:00", ...],
       ...
     }
     ```

Run your service in the background so it is actively listening when you finish.