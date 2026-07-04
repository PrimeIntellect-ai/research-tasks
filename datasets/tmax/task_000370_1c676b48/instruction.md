You are acting as a data scientist building an automated data pipeline. We have a local multi-service environment under `/app/` that consists of a log-emitting API and a Redis cache containing user metadata.

Your task is to write a Bash script `/home/user/pipeline.sh` that extracts, transforms, enriches, and samples data from these services, and then schedule it using `cron`.

**Environment details:**
- An API server is available at `http://127.0.0.1:8080/logs`. A GET request to this endpoint returns a large stream of JSON lines representing messy event logs. Example log:
  `{"timestamp": "2023-10-01T14:22:10Z", "user_id": "8472", "event_text": "  User CLICKED! ", "user_type": "guest"}`
- A Redis instance is running locally on port `6379`. It stores user categories. The key format is `user:<user_id>` (e.g., `user:8472`) and the value is a string (e.g., `premium`, `standard`, `spam`).

**Requirements for `/home/user/pipeline.sh`:**
1. **Extraction**: Fetch exactly 10,000 log lines from the API.
2. **Feature Extraction & Cleaning**:
   - Parse the `timestamp` to extract just the hour of the day (00-23) into a new field `hour`.
   - Clean the `event_text`: convert to lowercase, strip leading and trailing whitespace, and remove all punctuation (except spaces). Save this as `event_clean`.
3. **Enrichment**:
   - For each log, query Redis for the user's category using their `user_id`. If the key does not exist, use `"unknown"`. Save this as `user_category`.
4. **Stratified Sampling**:
   - The stream contains three `user_type`s: `guest`, `registered`, and `admin`.
   - Take a stratified sample of exactly 100 records for *each* `user_type` (300 records total).
5. **Output**:
   - Write the resulting dataset to `/home/user/cleaned_dataset.csv`.
   - The CSV must have the following header exactly, and be comma-separated:
     `hour,user_id,event_clean,user_category,user_type`
6. **Execution & Scheduling**:
   - Ensure the script is executable.
   - Run the script once so `/home/user/cleaned_dataset.csv` is generated.
   - Configure the user's crontab to run `/home/user/pipeline.sh` every 5 minutes.

**Services:**
You must first start the services by running `bash /app/services/start.sh`. Wait a few seconds for them to be fully ready before testing your script.

You may use common Linux utilities (like `jq`, `awk`, `redis-cli`, `curl`, `sed`). Make sure your final dataset strictly adheres to the format and stratification counts.