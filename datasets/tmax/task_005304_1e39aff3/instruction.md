You are a data analyst tasked with building a real-time data processing pipeline that normalizes and aggregates incoming streams of CSV log data. 

We have a legacy system that streams CSV logs. You need to create a service that receives these logs, processes them using a proprietary legacy binary, and exposes the aggregated results via an HTTP API.

Here are the requirements:
1. Create a service that listens for raw CSV data over TCP on `127.0.0.1:9000`. The incoming data stream will consist of newline-separated CSV records in the format: `timestamp,raw_id,action,duration`.
   - `timestamp` is an ISO8601 string.
   - `raw_id` is an integer.
   - `action` is a string.
   - `duration` is an integer representing seconds.

2. You must normalize the `raw_id` into a `canonical_id`. The logic for this mapping is locked inside a proprietary, stripped legacy binary located at `/app/id_mapper`. 
   - The `/app/id_mapper` executable reads integers from standard input (one `raw_id` per line) and prints the corresponding `canonical_id` to standard output (one per line). Because it is a compiled binary, you must interface with it efficiently as your pipeline streams data.

3. Keep a running aggregate of the total `duration` for each `canonical_id`.

4. Serve these running aggregations via an HTTP server listening on `127.0.0.1:9001`. 
   - Endpoint: `GET /aggregate?id=<canonical_id>`
   - Response format: A JSON object exactly like `{"canonical_id": 12345, "total_duration": 600}`. 
   - If a `canonical_id` has not been seen yet, return `{"canonical_id": <requested_id>, "total_duration": 0}`.

5. Set up a cron job for the `user` that runs every minute to save the current aggregation state to `/home/user/snapshot.json`. The format should be a JSON object mapping the string representation of `canonical_id` to the total `duration` (e.g., `{"12345": 600, "67890": 15}`).

Start both the TCP ingestion server and the HTTP API server in the background so that they are fully operational. Place all your code in `/home/user/pipeline/` (create the directory). You can use Python, Bash, or any other pre-installed languages to build the servers and glue everything together.