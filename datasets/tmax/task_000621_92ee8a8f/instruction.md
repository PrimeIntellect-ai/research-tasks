You are a platform engineer maintaining a CI/CD pipeline system. We have a Rust-based log aggregator service that connects to a local WebSocket server, parses build event streams using a finite state machine, and applies rate-limiting to prevent log spam. 

Currently, the Rust service at `/home/user/ci_aggregator` is failing. 

The WebSocket server (which you can start by running `python3 /home/user/mock_ci_server.py &`) listens on `ws://127.0.0.1:8080`. It emits JSON messages representing a build pipeline's states and metric data. 

The Rust service is supposed to:
1. Connect to `ws://127.0.0.1:8080`.
2. Parse incoming JSON messages. The messages have the format: `{"event": "STATE_NAME", "compute_cost": 15.5, "timestamp_ms": 1620000000}`.
3. Use a state machine that progresses strictly in this order: `START` -> `BUILD` -> `TEST` -> `DEPLOY` -> `END`. If it receives an event out of order (e.g., `TEST` before `BUILD`), it should be ignored entirely (do not add its cost).
4. Implement a simple rate limit: Ignore any message (even valid ones) that arrives within 50 milliseconds of the *previously accepted* valid message. 
5. Accumulate the total `compute_cost` (a floating-point number) of all valid, successfully processed events across all complete or incomplete pipeline runs.

There are bugs in `/home/user/ci_aggregator/src/main.rs`. The state machine logic is flawed, and the rate limiting is missing.

Your task:
1. Fix the Rust program in `/home/user/ci_aggregator` so it correctly implements the state machine, rate limiting, and mathematical aggregation.
2. Compile and run the Rust aggregator against the running mock server.
3. The mock server will automatically close the connection after sending all events. When the connection closes, your Rust program should write the final accumulated `compute_cost` (rounded to 2 decimal places) to `/home/user/final_cost.txt`.

Ensure your Rust program exits cleanly after the WebSocket closes.