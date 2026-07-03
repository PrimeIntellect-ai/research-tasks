You are an IT support engineer investigating a ticket escalated from the Data Engineering team. They have deployed a new Rust-based HTTP aggregator service, but it suffers from two intermittent issues:

1. **Floating-Point Inaccuracy**: The service occasionally returns slightly inaccurate results when summing large arrays of floating-point numbers with highly variable magnitudes.
2. **Resource Leak**: The service seems to leak async tasks or memory when upstream clients abort their requests mid-flight (cancellation).

We have provided the source code for the current buggy service in `/home/user/aggregator`. 

You also have access to a stripped, compiled binary of the legacy C++ service at `/app/legacy_oracle`. The data engineers noted that this legacy binary always produces the mathematically correct sum. If you pipe a JSON list of floats to its standard input, it will print the correct sum to standard output. Use this to delta-debug the inputs and figure out how to repair the floating-point precision in the Rust code.

Your tasks:
1. Identify and fix the floating-point precision bug in `/home/user/aggregator/src/main.rs`. Ensure the Rust service calculates sums that exactly match the output of `/app/legacy_oracle`.
2. Identify and fix the async task leak. Ensure that if a client disconnects prematurely, the server correctly cleans up and halts any spawned background processing for that request.
3. Build the fixed Rust service.
4. Run the fixed service in the background so it listens continuously on `127.0.0.1:8080`.

**Service Protocol Specifications:**
* **Listen Address:** `127.0.0.1:8080`
* **Endpoint:** `POST /aggregate`
* **Request Format:** JSON object containing an array of numbers. Example: `{"values": [1.0, 1e-10, 2.0]}`
* **Response Format:** JSON object with the precise sum. Example: `{"result": 3.0000000001}`
* **Endpoint:** `GET /health` must return HTTP 200 OK.

Leave the service running on port 8080 when you are finished. Automated tests will send complex HTTP requests, trigger cancellations, and verify that your service computes the correct sums without leaking memory or tasks.