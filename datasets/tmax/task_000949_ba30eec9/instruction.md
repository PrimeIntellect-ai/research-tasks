You are a data analyst managing a streaming data pipeline. Our current machine learning model is experiencing "data leakage" and crashing because it receives out-of-order timestamps and malformed data from our raw ingestion endpoints. 

You need to build a robust data sanitizer and ETL pipeline connector.

There are three services running in the background:
1. **Redis** (port 6379) - Used for state tracking by the consumer.
2. **Producer Service** (port 5000) - A simple HTTP service. Doing a `GET http://localhost:5000/data` returns a continuous stream of CSV rows.
3. **Consumer Service** (port 5001) - A TCP socket service. It expects clean CSV rows sent to it via standard TCP connection.

Your tasks:

1. **Write a Go CLI tool** at `/home/user/filter.go` (and compile it to `/home/user/filter`).
This tool must read a CSV stream from `stdin` and output valid rows to `stdout` in CSV format. 
The CSV has 5 columns: `transaction_id, timestamp, user_id, amount, category`.
It must enforce the following rules to prevent data leakage and pipeline crashes:
- Reject any row that does not have exactly 5 columns.
- Reject any row where `amount` cannot be parsed as a valid 64-bit float, or if the parsed float is negative (< 0).
- Reject any row where `category` contains any characters other than standard alphanumeric characters (`a-z, A-Z, 0-9`).
- **Data Leakage Prevention:** The `timestamp` column contains integer Unix timestamps. To prevent look-ahead data leakage in our rolling-window models, the stream must be strictly monotonically increasing. You must keep track of the maximum timestamp seen so far. Reject any row whose timestamp is less than or equal to the maximum timestamp already processed. (For the very first valid row, accept it and set the max timestamp to its value).
- Maintain the original CSV formatting for accepted rows.

2. **Write a pipeline script** at `/home/user/pipeline.sh`.
This bash script must continuously stream data from the Producer (`http://localhost:5000/data`), pipe it through your compiled `/home/user/filter` tool, and pipe the output to the Consumer service at `localhost:5001` using `nc`. 
Ensure the script is executable.

The automated verification will test your Go binary directly against a corpus of clean and adversarial files, and will also execute your `pipeline.sh` to ensure the end-to-end multi-service flow works.