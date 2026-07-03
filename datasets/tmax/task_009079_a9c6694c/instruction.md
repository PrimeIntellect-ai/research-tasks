You are an AI assistant helping a web developer fix a new real-time mathematical feature. 

The developer is building a backend service to compute the sum of squares of an array of numbers. For performance, the computation is written in Rust and exposed as a WebSocket server. A Python End-to-End (E2E) test script connects to this server, serializes a payload, and expects the mathematical result. 

However, the project is currently broken:
1. The Rust server (`/home/user/math_feature/server.rs`) fails to compile due to a classic ownership/borrow checker error.
2. The Python E2E test (`/home/user/math_feature/test_e2e.py`) currently has a small bug in how it serializes the mathematical payload before sending it over the WebSocket.

Your task:
1. Fix the Rust borrow checker error in `/home/user/math_feature/server.rs`.
2. Compile the Rust server (`rustc /home/user/math_feature/server.rs`) and start it in the background. It will bind to `ws://127.0.0.1:8765`.
3. Fix the Python test script `/home/user/math_feature/test_e2e.py` so that it correctly serializes the list `[2, 4, 6, 8]` into a JSON string under the key `"data"`, instead of sending a raw Python dictionary.
4. Run the Python E2E test script. 

When successful, the Python script will receive the correct mathematical result from the Rust server, deserialize it, and write the final result to `/home/user/math_success.log`. 

The task is complete when `/home/user/math_success.log` contains the correct sum of squares (which should be 120) in the format `RESULT: 120`. Do not modify the test script's assertion logic, only fix the serialization and the Rust compile error.