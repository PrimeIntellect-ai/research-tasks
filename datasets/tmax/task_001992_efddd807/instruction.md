You are tasked with porting a legacy C-based Linux telemetry processing tool into a minimal container environment by wrapping it in a modern Go REST API. 

Currently, we have a raw C library located at `/app/legacy/telemetry.c` and `/app/legacy/telemetry.h` that performs complex aggregations on arrays of sensor readings. We need to expose this via a Go-based web service, but there are a few major issues you need to resolve:

1. **Memory Safety Repair:** The legacy C code has a known memory safety issue (undefined behavior) that causes it to occasionally crash or return garbage data when processing certain inputs. You need to identify and fix the bug in `/app/legacy/telemetry.c`.
2. **Go REST API Construction:** Create a Go service in `/app/service/main.go` that uses `cgo` to interface with the repaired C library. 
   - The service must listen on `127.0.0.1:8080`.
   - It should expose a `POST /api/v1/process` endpoint.
   - The endpoint must accept a JSON payload: `{"batch_id": "string", "readings": [int, int, ...]}`.
   - All requests must be authenticated using the header `Authorization: Bearer dev_token_99z`.
3. **Multi-Service Integration:** The Go service must cache the output. A Redis instance is already configured to run on `127.0.0.1:6379`. Your Go API must connect to this Redis instance (no password) and store the processed aggregate result (an integer) under the key `batch:<batch_id>` before returning it in the HTTP response as `{"result": <int>}`.
4. **Build and Compose:** Modify the startup script at `/app/start.sh` so that it starts Redis in the background, compiles your Go application, and runs the Go service in the foreground.

Please implement the Go service, fix the C library, and ensure `/app/start.sh` cleanly brings up the entire composed system. We will verify your solution by running `/app/start.sh` and sending multiple concurrent HTTP requests to your Go API to ensure it processes data correctly without crashing.