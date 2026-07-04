You are a web developer tasked with building a specialized metrics collection service in Go. The service receives telemetry and low-level diagnostic payloads from embedded devices via WebSockets.

Here is what you need to build:

1. **Token Extraction**:
   There is a scanned configuration ticket located at `/app/auth_ticket.png`. The image contains an alphanumeric authorization token. Extract this token (you can use `tesseract`, which is preinstalled) as you will need it to secure your service.

2. **WebSocket Server**:
   Create a Go application that starts an HTTP server listening strictly on `127.0.0.1:8080`.
   - The server must handle requests at the route `/ws/{device_id}`.
   - It must enforce Authentication. Any HTTP upgrade request must contain the header `Authorization: Bearer <TOKEN>`, where `<TOKEN>` is the exact string you extracted from `/app/auth_ticket.png`. If the token is missing or incorrect, reject the request with an HTTP 401 Unauthorized status.
   - Upon successful authentication, upgrade the connection to a WebSocket.

3. **Assembly Diagnostic Analysis**:
   Once connected, the embedded devices will send JSON payloads containing raw x86-64 machine code instructions (in hexadecimal representation) that failed on the device.
   The incoming message format will be: `{"id": "msg_123", "hex_code": "48c7c00100000048c7c302000000"}`
   
   For each message received:
   - Decode the hexadecimal machine code.
   - Analyze the machine code instructions to count how many `mov` instructions (including variants like `movq`, `movabs`, etc.) are present in the snippet. (Hint: you can shell out to `objdump` or use a library like `golang.org/x/arch/x86/x86asm`).
   - Send a JSON response back over the WebSocket: `{"id": "msg_123", "mov_count": 2}`.

4. **Concurrent Logging**:
   You must keep an append-only audit log of all processed messages across all devices.
   - Use Go concurrency patterns (e.g., a dedicated goroutine and a channel) to safely aggregate the results from all active WebSocket connections without locking the handlers.
   - Append each processed result to a JSON Lines file at `/app/telemetry.log`.
   - Each line in the log must look exactly like this: `{"device_id": "<device_id_from_url>", "msg_id": "<id_from_payload>", "mov_count": <count>}`.

Ensure your Go application is built and running continuously in the background so it can be tested. You may use any third-party Go libraries (like `github.com/gorilla/websocket`) by initializing a Go module.