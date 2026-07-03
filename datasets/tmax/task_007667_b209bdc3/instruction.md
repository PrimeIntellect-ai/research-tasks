You are a log analyst tasked with building a scalable log processing pipeline. We have several raw log files in `/home/user/logs/` named `access_<id>.log`. 

The logs are in a comma-separated format:
`timestamp,endpoint,status_code,response_size`
Example:
`2023-10-01T10:00:05Z,/api/v1/data,200,1024`

Your task is to build a multi-language processing pipeline with the following requirements:

1. **Data Processing Script (`/home/user/process.py`)**:
   - Write a Python script that reads multiple log file paths passed as command-line arguments.
   - It must compute rolling 5-minute window statistics for every distinct minute present in the logs.
   - For a given minute `M` (truncated to the minute, e.g., `2023-10-01T10:05:00Z`), the 5-minute window includes all logs from `M - 4 minutes` up to and including the end of `M` (e.g., `2023-10-01T10:01:00Z` to `2023-10-01T10:05:59Z`).
   - For each minute window, calculate:
     - `total_requests`: Total number of requests in the window.
     - `error_rate`: Ratio of 5xx status codes to total requests, rounded to 4 decimal places.
     - `avg_response_size`: Average response size in bytes, rounded to 1 decimal place.
   - Process the files in parallel (using `multiprocessing` or `concurrent.futures`) to simulate handling large datasets.
   - Save the final aggregated output as a JSON file at `/home/user/stats.json`. The format must be a dictionary keyed by the minute string (e.g., `"2023-10-01T10:05:00Z"`) containing the calculated metrics. Example:
     ```json
     {
       "2023-10-01T10:05:00Z": {
         "total_requests": 150,
         "error_rate": 0.0200,
         "avg_response_size": 1024.5
       }
     }
     ```

2. **Pipeline Script (`/home/user/pipeline.sh`)**:
   - Create a Bash script that finds all `access_*.log` files in `/home/user/logs/` and passes them as arguments to your `process.py` script.
   - Ensure the script is executable.

3. **Cron Schedule (`/home/user/crontab.txt`)**:
   - Write a single valid crontab entry into `/home/user/crontab.txt` that schedules `/home/user/pipeline.sh` to run every 5 minutes.

Run your `pipeline.sh` manually once to generate the `/home/user/stats.json` file for verification.