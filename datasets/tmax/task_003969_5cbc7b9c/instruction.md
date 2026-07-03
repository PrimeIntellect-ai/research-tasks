A customer has deployed our new C++ telemetry ingestion pipeline, but they are reporting multiple issues. First, the ingestor occasionally crashes under load due to what looks like concurrency issues, and it fails to properly decode certain serialized payloads. Second, we need to add a mandatory sanitization layer to this pipeline to filter out malicious payloads that attempt exploit downstream log viewers.

You are acting as a support engineer. The customer has provided a packaged environment under `/app/telemetry_env`. Inside, you will find:
- A `generator.sh` script that simulates multiple backend nodes sending telemetry data via UDP (Service A).
- A `sink.sh` script that simulates the downstream storage backend listening on TCP (Service C).
- The source code for the `telemetry_ingestor` (Service B) in `/app/telemetry_env/src/`.

Your tasks:
1. **Debug and Fix the Ingestor**: 
   - Fix the dependency conflict in `/app/telemetry_env/src/Makefile` (it is linking an incompatible version of the serialization library).
   - Resolve the race condition in the worker pool of `ingestor.cpp` that causes intermittent crashes.
   - Fix the decoding function where UTF-8 boundary errors cause serialization to fail. Include intermediate assertions (`assert()`) to validate the payload boundaries before decoding.

2. **Implement Sanitization (Adversarial Filter)**:
   - Modify the ingestor to classify and drop malicious payloads.
   - We have provided two directories of raw telemetry payloads: `/app/telemetry_env/corpora/clean/` (valid telemetry) and `/app/telemetry_env/corpora/evil/` (containing shellcode, directory traversal strings, and invalid escape sequences).
   - Your filter must allow 100% of the `clean` payloads to be forwarded to the sink, and drop 100% of the `evil` payloads. When a payload is dropped, write a single line to `/tmp/dropped_payloads.log` with the format `DROPPED: <payload_id>`.

3. **End-to-End Integration**:
   - Recompile the ingestor.
   - The ingestor must listen on `UDP port 8080` and forward valid payloads to `TCP port 9090` (where `sink.sh` listens).
   - Start `sink.sh`, start your fixed `telemetry_ingestor`, and run `generator.sh` to pump data through the pipeline.

Provide the final working C++ code and ensure all services are running properly so the automated test can verify the end-to-end flow and check `/tmp/dropped_payloads.log` against the corpora.