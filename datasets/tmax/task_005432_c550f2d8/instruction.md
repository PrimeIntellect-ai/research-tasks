You are a data analyst setting up an automated data extraction and serving pipeline. We have a directory of daily sales reports in CSV format from different international branches, and they are notoriously messy with character encodings.

Your objectives:

1. **Extract Configuration:** We received a scanned memo with our new security protocol. It is located at `/app/config_memo.png`. Use OCR (e.g., `tesseract`, which is installed) to extract the secret API token from this image. It will be in the format `API_TOKEN: <token>`.

2. **Develop the Data API:** Write a Python HTTP web service (using Flask, FastAPI, or the standard library) that listens on `127.0.0.1:5000`. Run this service in the background so it remains active.

3. **API Specifications:**
   - Endpoint: `GET /rolling_stats`
   - Authentication: Must enforce the `Authorization: Bearer <token>` header using the exact token extracted from the image. If missing or incorrect, return a 401 Unauthorized status.
   - Processing Logic: When the endpoint is called, it must dynamically read all CSV files located in `/app/data/`. 
   - The CSVs have varying character encodings (e.g., UTF-8, UTF-16, Shift-JIS) but all share two columns: `date` (YYYY-MM-DD) and `amount` (float). You must correctly read and decode all of them, combine the records, and sort them chronologically by date.
   - Compute a 3-day rolling average (the current day and the previous 2 days) for the `amount` column.
   - The API must write the combined, sorted data (including the newly computed rolling average column) to `/home/user/processed_data.parquet` in Parquet format.
   - The API must return a JSON response containing the rolling average for the latest date in the dataset. Format: `{"latest_date": "YYYY-MM-DD", "rolling_avg_3d": <float>}`.

4. **Cron Scheduling:** To ensure our backup scripts run on schedule, create a file at `/home/user/cron_schedule.txt` containing exactly one crontab line that schedules the command `/bin/bash /home/user/backup.sh` to run at exactly 4:30 AM every Tuesday.

Ensure your service is running and bound to `127.0.0.1:5000` before concluding your final turn.