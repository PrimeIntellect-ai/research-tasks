You are a performance engineer tasked with debugging a legacy Bash-based metric analysis service. The service is supposed to calculate statistical anomalies in request latencies, but it's currently returning incorrect results and failing to authenticate properly.

We have an old screenshot of the internal dashboard at `/app/auth_screenshot.png` which contains the hardcoded API token required to access the service. 

Here is what you need to do:

1. **Extract the Auth Token**: Read the API token from `/app/auth_screenshot.png` (using OCR tools like `tesseract`). 

2. **Debug the Metric Processor**: 
   There is a script at `/home/user/handle_req.sh`. This script is executed for every incoming HTTP request. It expects an HTTP POST request with a payload of comma-separated values (`endpoint,latency`).
   Currently, the script has format parsing edge-cases: some upstream systems send the latency purely as an integer (e.g., `120`), while others append units with arbitrary spaces (e.g., `120ms`, ` 120 ms`, `120.0`). 
   Fix the Bash/awk logic in `/home/user/handle_req.sh` to correctly strip these units and calculate the mathematical average of all latencies in the payload. It should return an HTTP 200 response with a JSON payload in the format: `{"average": 120}` (rounded to the nearest integer).

3. **Enforce Authentication**: Update `/home/user/handle_req.sh` to check the `Authorization: Bearer <TOKEN>` HTTP header. If the token does not exactly match the one found in the screenshot, return an `HTTP/1.1 401 Unauthorized` response.

4. **Deploy the Service**: Once fixed, bind the service to port `9090` using `socat` so it can receive actual network requests. Run the server in the background so it stays alive for verification:
   `socat TCP-LISTEN:9090,reuseaddr,fork EXEC:/home/user/handle_req.sh &`

Make sure the server is actively listening on `127.0.0.1:9090` when you finish. Do not close the terminal or kill the background process.