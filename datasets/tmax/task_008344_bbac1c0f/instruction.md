You are an integration developer tasked with exposing a legacy C-based security module as a modern REST API, and setting up a reverse proxy to route traffic to it.

A legacy C library source exists in `/home/user/legacy`. It provides a function `get_encoded_secret()` that returns a hardcoded security token. The token is encoded using a custom legacy format: it is an ASCII Hex string, and when decoded to bytes, each byte has been XOR'd with the value `0x55`.

Your task involves the following steps:

1. **Build the C Library**:
   Compile the C code in `/home/user/legacy` (which contains `secret.c` and `secret.h`) into a shared library named `libsecret.so` located in `/home/user/legacy`.

2. **Create the Go API Service**:
   Write a Go application in `/home/user/api/main.go` that:
   - Uses `cgo` and links against `libsecret.so` to call `get_encoded_secret()`.
   - Decodes the hex string and reverses the XOR `0x55` cipher to recover the original UTF-8 string.
   - Starts an HTTP server on `127.0.0.1:8080`.
   - On a `GET /secret` request, serializes the decrypted string into the following JSON response:
     `{"status": "success", "data": "<decrypted_string>"}`
   - Sets the `Content-Type: application/json` header.

3. **Create the Go Reverse Proxy**:
   Write a second Go application in `/home/user/proxy/main.go` that acts as a reverse proxy:
   - Listens on `127.0.0.1:9090`.
   - Forwards all incoming HTTP requests to the API service at `127.0.0.1:8080`.
   - Injects a custom HTTP response header: `X-Proxy-Routed: true` to the response returned to the client.

4. **Verify the Integration**:
   Run both Go applications in the background. Then, execute a `curl` command to the reverse proxy to fetch the secret and save the exact HTTP response body to `/home/user/final_output.json`. 

Ensure all applications are running and the output file is created successfully.