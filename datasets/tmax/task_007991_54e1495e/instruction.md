You are acting as a Release Manager building a deployment verification bridge. Before we can release our microservices, we need an automated pipeline that calculates a "deployment readiness score" using a legacy C library, a Python gRPC internal service, and a Node.js API/WebSocket gateway for external integration.

Your task is to implement this multi-language architecture from scratch in the `/home/user/deploy_bridge` directory. 

Here are the detailed specifications for the components you must create:

1. **Shared Library & ABI Management (C)**
Create a C file named `readiness.c` and compile it into a shared library named `libreadiness.so`.
- It must export a single function: `int calculate_score(const char* service_name, int version);`
- The function must calculate and return the score using this exact formula: the length of the string `service_name` multiplied by the `version`. (e.g., "auth", version 3 -> 4 * 3 = 12).

2. **gRPC and Protobuf Service (Python)**
Create a Protobuf file named `deployment.proto` defining:
- A service named `ReadinessService`.
- A method named `Check` that takes a request message containing `string service_name` and `int32 version`, and returns a response message containing `int32 score`.

Create a Python gRPC server named `grpc_server.py`:
- It must listen on `localhost:50051`.
- It must implement the `ReadinessService`.
- It must use `ctypes` to load `libreadiness.so` and call `calculate_score` to determine the score to return.

3. **URL Routing and WebSocket Gateway (Node.js)**
Create a Node.js server named `gateway.js` that listens on port `3000`.
- **HTTP Routing:** Implement a `GET /check/:service/:version` endpoint. When hit, it must parse the URL parameters, make a gRPC call to the Python server, and return the score as a JSON response: `{"score": <result>}`.
- **WebSocket:** Implement a WebSocket server on the path `/ws`. Whenever the HTTP endpoint is successfully hit and a score is retrieved, the server must broadcast a JSON message to all connected WebSocket clients in this exact format: `{"event": "deployment_checked", "service": "<service_name>", "version": <version>, "score": <score>}`.

4. **Integration Testing**
Write a Node.js integration test script named `run_test.js` that:
- Connects to the WebSocket at `ws://localhost:3000/ws`.
- Makes an HTTP GET request to `http://localhost:3000/check/billing-service/4`.
- Captures the broadcasted WebSocket message.
- Writes the exact received WebSocket JSON string to a file named `/home/user/deploy_bridge/test_result.log`.
- Exits cleanly.

**Constraints & Setup:**
- Create the directory `/home/user/deploy_bridge` and work entirely within it.
- You may install any necessary dependencies using `pip` (e.g., `grpcio`, `grpcio-tools`) and `npm` (e.g., `express`, `ws`, `@grpc/grpc-js`, `@grpc/proto-loader`).
- You must start the Python and Node.js servers in the background before running your test script.
- The final verification relies *solely* on the contents of `/home/user/deploy_bridge/test_result.log` produced by your integration test. Make sure it matches the exact JSON structure specified above.