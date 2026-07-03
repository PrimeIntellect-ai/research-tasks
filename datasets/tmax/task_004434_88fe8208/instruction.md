You are helping me migrate an internal legacy testing tool from Python 2 to Python 3. 

We have a multi-service architecture located in `/home/user/app/`. 
1. A backend service written in Go (already compiled and running on `127.0.0.1:8081` via our startup script). It handles high-concurrency tasks using goroutines.
2. A Python reverse-proxy and protocol translation service in `/home/user/app/proxy/`.

Your task is to upgrade the Python service to Python 3 and fix its routing and serialization bugs.

Here is what you need to do:
1. **Migrate the Code:** The proxy server code is at `/home/user/app/proxy/server.py`. It is currently written in Python 2. Refactor it to be valid Python 3 code. Resolve any module import changes (e.g., `BaseHTTPServer` to `http.server`, `urllib2` to `urllib.request`).
2. **Implement the HTTP Proxy:** The proxy must listen for HTTP requests on `127.0.0.1:8080`. For every incoming HTTP request, it should forward it to the Go backend at `http://127.0.0.1:8081`, but it MUST inject a new HTTP header: `X-Migrated-By: Python3` before forwarding. It should then return the exact backend response to the client.
3. **Implement the TCP Translator:** The proxy must also listen for raw TCP connections on `127.0.0.1:9090`. The incoming protocol consists of a 4-byte big-endian integer representing the payload length, followed by a `pickle` serialized dictionary. 
   - Note: Because the clients are still running Python 2, the pickled payload was generated in Python 2. You must safely deserialize this in Python 3 (pay attention to `bytes` vs `str` decoding, specifically using `encoding='bytes'` or `latin1`).
   - The dictionary will contain a `{"route": "/somepath", "data": "payload"}`.
   - The proxy must extract the `route`, make a `POST` request to `http://127.0.0.1:8081<route>` with the `data` as a JSON body, and then serialize the Go backend's JSON response using `pickle` (protocol 2, for backward compatibility) and send it back over the TCP connection with the 4-byte length prefix.
4. **Run the Service:** Ensure your migrated proxy service is running in the background. Do not stop the Go backend. 

Your final result must be a running Python 3 process listening on `8080` (HTTP) and `9090` (TCP), successfully proxying requests to the Go backend on `8081`. 

Leave the proxy running when you are done.