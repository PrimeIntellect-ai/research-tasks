I am a release manager preparing our new "Payload Analyzer" microservice for staging deployment. Before we can release it, I need you to build the core service, write unit tests for the numerical algorithm, and set up a secure reverse proxy to front the application. 

All code must be written in Go. You will need to create two separate Go modules in the following directories:
1. `/home/user/analyzer/` - The backend service.
2. `/home/user/proxy/` - The reverse proxy service.

Here are the requirements:

**Phase 1: The Numerical Algorithm & Backend Service (/home/user/analyzer/)**
1. Initialize a Go module named `analyzer`.
2. Create a file `entropy.go` containing a function `CalculateEntropy(data []byte) float64`. It must calculate the Shannon entropy of the given byte slice.
   * Shannon entropy formula: $H = - \sum (p_i \log_2 p_i)$, where $p_i$ is the probability (frequency) of each unique byte in the data. If the input is empty, return 0.
3. Create a test file `entropy_test.go` with unit tests for `CalculateEntropy`. Ensure you test at least these two cases:
   * Data: `[]byte{0x00, 0x00, 0x00, 0x00}` -> Expected Entropy: `0.0`
   * Data: `[]byte{0x00, 0x11, 0x22, 0x33}` -> Expected Entropy: `2.0`
4. Create `main.go` that starts an HTTP server on port `9000`. It must expose a `POST` endpoint at `/entropy`.
   * It should accept a JSON body: `{"data": "<hex_encoded_string>"}`.
   * It should decode the hex string, calculate the entropy using your function, and return JSON: `{"entropy": <float64_value>}`.

**Phase 2: The Reverse Proxy (/home/user/proxy/)**
1. Initialize a Go module named `proxy`.
2. Create `main.go` that starts an HTTP reverse proxy server on port `8080`.
3. The proxy must forward any requests sent to `/api/entropy` to the backend service at `http://localhost:9000/entropy`.
4. As a security requirement for the release, the proxy MUST inject the following HTTP response header into all responses returned to the client:
   `X-Deployment-Sec: Ready`

**Phase 3: Building, Running, and Verification**
1. Run `go test -v ./...` inside `/home/user/analyzer/` and redirect the output to `/home/user/test_results.log`.
2. Start both the backend service and the reverse proxy in the background.
3. Use `curl` to test the reverse proxy. Send a POST request to `http://localhost:8080/api/entropy` with the JSON payload `{"data": "00112233"}`. Include the `-i` flag to capture headers. Save the complete `curl` output (headers and body) to `/home/user/proxy_test.log`.

Make sure all services are running and the log files are accurately created at the exact paths specified.