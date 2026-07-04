You are a data scientist tasked with building and deploying a real-time data anonymization and aggregation pipeline for user activity logs. The system consists of multiple cooperating local services, but the current pipeline is disconnected and lacks a critical sanitization step.

Your objective is to write the core data processor in C, validate it against a test corpus, and orchestrate the pipeline services to achieve a working end-to-end flow.

### System Architecture
The environment contains the following services and files (which you can start using `/app/start_services.sh`):
1. **Log Producer**: A Python service running on `localhost:9001`. Upon connection, it streams raw JSON user activity logs.
2. **Redis**: Running on `localhost:6379`. Used as an intermediate message broker.
3. **Stats API**: A Flask application running on `localhost:8080`. It reads from the Redis list `cleaned_logs`, computes summary statistics, and serves them at `http://localhost:8080/stats`.

### Step 1: Write the C Sanitizer
Write a C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`. It must read JSON log lines from `stdin` (one per line) and write processed lines to `stdout`.

Your C program must implement the following logic:
1. **Data Masking (SSN)**: Find any `"ssn": "DDD-DD-DDDD"` (where D is a digit) and replace the value with `"XXX-XX-XXXX"`.
2. **Data Masking (Email)**: Find any `"email": "string@domain.com"` and replace the local part with `***`, keeping the domain (e.g., `"email": "***@domain.com"`).
3. **Time-based Bucketing**: Extract the `"timestamp"` field (format: `YYYY-MM-DDTHH:MM:SSZ`) and append a new field `"time_bucket": "YYYY-MM-DDTHH:MM"` to the end of the JSON object, right before the closing `}`. 

*Constraint*: Your sanitizer must be robust. It must not modify fields that look vaguely like SSNs or emails but aren't (e.g., `"product_code": "123-45-6789"` must remain untouched). You may use standard POSIX libraries (like `<regex.h>`).

### Step 2: Validate against the Corpora
Your sanitizer must pass strict adversarial checks. 
- Clean corpus: `/app/data/clean_logs.txt` (Must be output exactly as input, plus the `time_bucket` field).
- Evil corpus: `/app/data/evil_logs.txt` (Must have PII masked exactly as specified, plus the `time_bucket` field).

### Step 3: Pipeline DAG Orchestration
Create a bash script at `/home/user/pipeline.sh` that connects the services. The script should:
1. Read the stream from the Log Producer (`localhost:9001`).
2. Pipe the stream through your `/home/user/sanitizer`.
3. Push each sanitized JSON line into the Redis list named `cleaned_logs` (you can use `redis-cli -x rpush cleaned_logs`).

### Step 4: End-to-End Execution
1. Run `/app/start_services.sh`.
2. Run your `/home/user/pipeline.sh` for at least 5 seconds to process the batch of logs.
3. Query the Stats API using `curl http://localhost:8080/stats` and save the output to `/home/user/final_stats.json`.