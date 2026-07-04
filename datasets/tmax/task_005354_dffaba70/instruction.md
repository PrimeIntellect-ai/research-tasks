You are an integration developer tasked with creating a secure C++ REST API wrapper around a legacy, proprietary mathematical binary.

We have a legacy tool located at `/app/risk_calc`. It is a stripped Linux executable that calculates a proprietary financial risk score. It accepts exactly three command-line arguments in this order: `price` (float), `volatility` (float), and `time` (float). It prints a single floating-point number to standard output and exits with code 0 on success.

Your task is to write a C++ HTTP server that exposes this mathematical oracle over the network, incorporating strict request validation and rate limiting.

### API Requirements
1. **Server Configuration:** 
   - Write your C++ server in `/home/user/server.cpp`.
   - Compile it to `/home/user/api_server` using standard `g++`.
   - The server must listen on `0.0.0.0:9090`.
   - (You may download and use single-header libraries like `httplib.h` or `json.hpp` from their official repositories).

2. **Endpoint:**
   - Expose exactly one endpoint: `POST /api/v1/calculate`

3. **Authentication:**
   - Clients must pass the header `Authorization: Bearer secret-math-key`.
   - Return HTTP `401 Unauthorized` if the header is missing or incorrect.

4. **Payload & Request Validation:**
   - Accept a JSON body with three numeric keys: `price`, `vol`, and `time`.
   - Return HTTP `400 Bad Request` if the body is invalid JSON or missing any of these keys.
   - Enforce the following mathematical constraints:
     - `price`: Must be between `0.0` and `10000.0` (inclusive).
     - `vol`: Must be strictly greater than `0.0` and less than or equal to `2.0`.
     - `time`: Must be between `0.1` and `30.0` (inclusive).
   - Return HTTP `400 Bad Request` if any constraint is violated.

5. **Rate Limiting:**
   - Implement an in-memory per-IP rate limiter.
   - An IP address may make a maximum of 3 requests per second.
   - If an IP exceeds this limit, immediately return HTTP `429 Too Many Requests`.

6. **Execution & Response:**
   - If the request is valid and within limits, invoke `/app/risk_calc <price> <vol> <time>`.
   - Parse the floating-point output.
   - Return an HTTP `200 OK` response with the JSON payload: `{"result": <computed_value>}`.

### Verification
Once you have written the code, compiled it, and verified it works (e.g., using `curl`), leave the `/home/user/api_server` process running in the background. Automated verification will connect to port 9090 using HTTP, test the authentication, submit boundary-testing mathematical inputs, and deliberately trigger your rate limiter.