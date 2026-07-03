You are a deployment engineer tasked with rolling out an update to our data ingestion pipeline. The pipeline consists of three components:
1. A Redis container acting as an in-memory buffer.
2. A Data Emitter service that generates mock sensor data and writes it to Redis.
3. A Processor script that reads this data from Redis, performs transformations, and writes it to disk.

The services are pre-configured in `/app/`. Your task involves fixing the pipeline, enforcing strict storage permissions, and optimizing the Python processor.

Step 1: Environment Setup & Permissions
- Run `/app/start_services.sh` to initialize the Redis instance and the Data Emitter. The Emitter will immediately populate Redis with 50,000 records (keys: `sensor:0` to `sensor:49999`).
- Create an output directory exactly at `/home/user/output_data/`.
- Use Access Control Lists (ACLs) to configure permissions on `/home/user/output_data/`. Set it so the current user (`user`) has full read/write/execute permissions, and the `nobody` user has strictly read and execute permissions (`r-x`). Ensure default ACLs for newly created files inside this directory give `nobody` read access (`r--`).

Step 2: Processor Implementation & Optimization
The naive processor at `/app/processor/naive_processor.py` is too slow and currently fails to connect because it defaults to the wrong Redis host/port and fails to check storage constraints. 
Write an optimized script at `/home/user/optimized_processor.py` (in Python) that does the following:
- Connectivity: Connects to the local Redis instance (the emitter runs Redis on `127.0.0.1:6379`).
- Storage Check: Uses Python's `shutil` or `os` modules to check the available disk space on the partition hosting `/home/user/output_data/`. If the available space is less than 50MB, the script must immediately terminate with exit code `2`.
- Data Processing: Reads all 50,000 records (`sensor:0` to `sensor:49999`) from Redis. You MUST optimize this retrieval (e.g., using Redis pipelining or MGET) because standard sequential GETs are too slow to pass the performance benchmark.
- Data Transformation: For each record, decode the JSON payload, multiply the `"value"` field by `1.5`, and append the JSON string `{"id": <id>, "processed_value": <new_value>}` to a single file `/home/user/output_data/processed.jsonl` (one JSON object per line).

Step 3: Verification
Once your script is ready, run the benchmark tool: `/app/benchmark.py /home/user/optimized_processor.py`. 
To pass the deployment check, your script must process all 50,000 records and exit in under 1.5 seconds.
Leave the system running with the processed file generated at `/home/user/output_data/processed.jsonl`.