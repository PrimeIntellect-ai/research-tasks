You are an on-call engineer responding to a 3am PagerDuty alert. The primary telemetry aggregation pipeline has completely stalled.

System Overview:
We have a multi-service telemetry pipeline located in `/app/`:
1. **Message Broker**: A Redis instance.
2. **Ingestion Service**: A FastAPI service (`/app/ingest/main.py`) that receives JSON telemetry via HTTP POST on port 8000 and pushes it to a Redis list `telemetry_queue`.
3. **Aggregation Worker**: A Python service (`/app/worker/main.py`) that pops data from Redis, parses a custom hex-encoded payload inside the telemetry, and serves the aggregated metrics via a gRPC server on port 50051.

The Incident:
A recent batch of telemetry data caused the Aggregation Worker to hang indefinitely, spiking CPU to 100% and completely halting the processing queue. The unprocessed batch of 2,000 JSON payloads has been dumped to `/app/data/failed_batch.json`.

Your Objectives:
1. **Diagnose and Fix**: Use delta debugging or bisection on the `failed_batch.json` payloads to identify which specific record causes the infinite loop in the parser (`/app/worker/parser.py`). Fix the parsing logic so it safely skips or handles malformed/edge-case payloads without looping infinitely or crashing.
2. **Bring Up Services**: 
   - Start the Redis server daemonized.
   - Start the Ingestion Service on `127.0.0.1:8000`.
   - Start the Aggregation Worker gRPC service on `127.0.0.1:50051`.
3. **Verify Functionality**: Re-ingest the `failed_batch.json` data by sending it to the FastAPI endpoint to ensure it processes successfully.

Leave the three services running. Our automated verifier will issue real HTTP requests to port 8000 and gRPC requests to port 50051 to confirm the system's stability and correct data transformation.

Make sure you do not change the gRPC protobuf definitions, only the internal logic of the parser.