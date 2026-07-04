You are a data engineer tasked with fixing a broken mathematical ETL pipeline. 

We have a multi-service architecture located in `/home/user/app/` that ingests user transaction events, processes them into tabular features, and trains a basic fraud-detection model. The system consists of:
1. **Redis**: Message broker.
2. **Ingestion API**: A web service on port 5000 that receives JSON payloads and queues them in Redis.
3. **ETL Worker**: A Python service that pops from Redis, converts the data using Pandas, and writes to an SQLite database (`/home/user/app/db/transactions.db`).

**The Problem:**
Our downstream mathematical models are failing because the integer columns (`age` and `clicks`) in our SQLite database are silently being converted to `FLOAT`. This happens because the API is accepting malformed JSON where `age` or `clicks` are submitted as `null`, strings (e.g., `"25"`), or floats (e.g., `25.0`). When Pandas aggregates this, the missing/invalid values cause silent NaN introduction, which forces the entire column's dtype to upcast from `int64` to `float64`.

Your objectives:

**Part 1: Build a Strict Sanitizer (Adversarial Filter)**
Create an executable shell script at `/home/user/validate.sh`.
This script must accept a single argument: the path to a JSON file containing a transaction payload.
- It must exit with status code `0` (Clean) if AND ONLY IF:
  - `age` is a strict JSON integer (not a string, not a float, not null).
  - `clicks` is a strict JSON integer.
  - `amount` is a number (integer or float is fine).
- It must exit with status code `1` (Evil/Malformed) for any other case (e.g., missing fields, nulls, wrong types).
*Hint: You can use `jq` to inspect JSON types.*

**Part 2: Fix and Reconfigure the Services**
The multi-service composition is currently failing to start and route data correctly. 
1. Fix the networking: The Ingestion API is currently configured to look for Redis on the wrong port. Update `/home/user/app/config.env` so that `REDIS_PORT` matches the actual default Redis port (6379).
2. Wire the sanitizer: The Ingestion API supports an external validation script. In `/home/user/app/config.env`, set `VALIDATOR_SCRIPT=/home/user/validate.sh`.
3. Start the services by running `/home/user/app/start_services.sh`.

Once you have written the script, fixed the config, and started the services, use `curl` to send a few test requests to `http://localhost:5000/ingest` to ensure your end-to-end flow works. The automated verifier will directly test `/home/user/validate.sh` against a hidden corpus of clean and evil JSON files, and will also send traffic to your API to verify the multi-service pipeline.