You are a mobile build engineer maintaining the team's build telemetry pipelines. To monitor the build farm efficiently without overloading the central dashboard, the team is developing a lightweight WebSocket broker in C. This broker receives JSON metrics from build worker nodes, evaluates them against a dynamic filter expression, enforces a rate limit, and drops messages that violate these rules.

Your codebase is located in `/home/user/telemetry_broker`. It contains a partially implemented WebSocket server `server.c`, an incomplete `Makefile`, and a Python test script `test_runner.py`.

Your tasks:
1. **Dependency Management**: Install the required C libraries for WebSocket support and JSON parsing. The project relies on `libwebsockets` and `jansson`. Update the `Makefile` so that `make` successfully builds the `telemetry_broker` executable using `pkg-config` for these two libraries.
2. **Expression Parsing and Evaluation**: Implement the `evaluate_filter` function in `server.c`. 
   - It takes a Jansson JSON object (`json_t *`) and a filter expression string.
   - The expression format is strictly `KEY<OP>VALUE` (e.g., `warnings<10`, `apk_size>50000`, `errors==0`). 
   - `KEY` is a JSON object key. `OP` is one of `<`, `>`, or `==`. `VALUE` is an integer. 
   - Return 1 if the JSON object contains the `KEY` with an integer value that satisfies the expression, and 0 otherwise.
3. **Request Validation & Rate Limiting**: Implement the `check_rate_limit` function in `server.c`.
   - Each WebSocket session has an associated `struct per_session_data` (already defined in `server.c`).
   - Implement a rolling window rate limit: allow a maximum of **3 messages per 1000 milliseconds** per connection.
   - Return 1 if the message is allowed, or 0 if it should be dropped due to rate limiting.
4. **Benchmarking & Validation**: 
   - Compile the broker.
   - Run the broker in the background: `./telemetry_broker 8080 "warnings<5" &`
   - Execute the test and benchmark script: `python3 test_runner.py`. This script connects via WebSockets, blasts messages to test the rate limiter, sends various JSON payloads to test the filter, and writes the final summary to `/home/user/telemetry_broker/validation.log`.

Make sure `/home/user/telemetry_broker/validation.log` contains the string `SUCCESS: All tests passed.` when you are done.