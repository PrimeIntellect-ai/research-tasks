You are helping a developer migrate a legacy Python 2 system to Python 3. As part of this migration, they need a fast, local "Python 2 emulator" service written in Rust to handle specific legacy semantics (specifically, integer division and lack of parentheses in `print` statements) without needing to spawn full Python 2 processes. 

To integrate with the new Python 3 microservices, this Rust emulator must be served over WebSockets and placed behind a local reverse proxy.

Your task is to complete the system:

1. **Implement the Python 2 Emulator in Rust:**
   In `/home/user/py2_evaluator`, a `Cargo.toml` and an empty `src/main.rs` are waiting for you. 
   Write a Rust application that starts a WebSocket server on `127.0.0.1:8081`. 
   For every incoming text message (a legacy Python 2 expression), evaluate it according to these strict rules:
   - If the message is exactly `print "STR"`, return the string `STR` (without quotes).
   - If the message is exactly `A / B` (where A and B are positive integers), return the result of integer division (Python 2 behavior) as a string. E.g., `5 / 2` -> `2`.
   - If the message is exactly `print A / B`, return the result of the integer division.
   Return "ERROR" for anything else. 
   *(Note: The Cargo.toml already includes `tokio` and `tokio-tungstenite` for your convenience).*
   Compile and run your Rust server in the background.

2. **Configure a Reverse Proxy:**
   Set up a reverse proxy using standard shell tools (like `socat`) that listens on `127.0.0.1:8080` (TCP) and forwards all traffic to your WebSocket server on `127.0.0.1:8081`. 
   Run this proxy in the background and save its PID to `/home/user/proxy.pid`.

3. **Benchmarking and Sorting:**
   I have provided a script at `/home/user/benchmark.sh`. Once your proxy and server are running, execute this script. It will send multiple requests to `ws://127.0.0.1:8080` and append the response latency and result to `/home/user/raw_results.txt` in the format: `[latency_ms] [result]`.
   
   Once the benchmark finishes, sort `/home/user/raw_results.txt` numerically in **descending** order based on the latency column. Save the perfectly sorted output to `/home/user/sorted_results.txt`.

Ensure your proxy is running and `/home/user/sorted_results.txt` is created before finishing.