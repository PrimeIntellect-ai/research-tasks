You are an engineer investigating a critical issue in a long-running internal API service. The service is experiencing severe goroutine and memory leaks, ultimately leading to out-of-memory (OOM) crashes in production.

We have isolated a simplified version of the service code and placed it in `/app/vendored_service/`. The service is written in Go and exposes a `/process` endpoint that accepts JSON payloads.

Your analysis has revealed two distinct triggers for the resource leak:
1. **Client Cancellation:** When an upstream client prematurely drops the connection or cancels the HTTP request while the service is processing it, a goroutine is permanently leaked.
2. **Corrupted Input:** If a client sends a malformed or corrupted JSON payload (e.g., incomplete objects or syntax errors) and drops the connection, the service CPU spikes and a goroutine is locked in an infinite state.

Your task:
1. Diagnose and fix the encoding/serialization handling loop to properly recover from corrupted JSON input instead of hanging. It should return an HTTP 400 status code on bad JSON.
2. Fix the intermediate state tracing and concurrency logic so that when a client cancels a request, no background worker goroutines or channels are left blocked forever.
3. Build and start the fixed service so that it listens on `127.0.0.1:8080`.
4. Leave the service running.

The automated verification system will issue real protocol-level requests to your service on port 8080. It will verify that valid requests succeed, corrupted requests return an error without causing a CPU loop, and cancelled requests do not increase the baseline goroutine count (exposed via the `/goroutines` endpoint).