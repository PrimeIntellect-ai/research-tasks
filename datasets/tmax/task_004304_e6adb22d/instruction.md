You are a network security engineer investigating a series of crashes in our custom traffic inspection proxy. We have a proprietary, stripped binary located at `/app/traffic_inspector` that is used to analyze incoming HTTP headers for malicious patterns. Recently, an attacker has been sending crafted payloads exploiting an open redirect vulnerability in our upstream web server's login flow, which unexpectedly causes the `traffic_inspector` binary to segment fault.

Your task is to build a robust C-based front-end proxy that sits in front of the `traffic_inspector`, sanitizes the traffic, and manages secure connections. 

Specifically, you must:
1. **Analyze the Binary**: Reverse-engineer or black-box test `/app/traffic_inspector` to determine the exact HTTP header payload (related to an open redirect) that causes it to crash. 
2. **TLS/SSL Management**: Generate a self-signed wildcard SSL certificate for `*.internal.corp` and configure your proxy to terminate TLS on port 8443 using this certificate. Store the cert at `/home/user/certs/server.crt` and the key at `/home/user/certs/server.key`.
3. **Write the Proxy in C**: Create a C program at `/home/user/proxy.c` (and compile it to `/home/user/proxy`) that:
   - Listens for raw HTTP requests on TCP port 8080 and HTTPS on port 8443.
   - Inspects the HTTP headers and cookies of incoming requests.
   - If a request contains the payload that crashes the `traffic_inspector` (e.g., a specific malicious `Location` or `Referer` header), the proxy must immediately drop the connection and append a log entry to `/home/user/security_drops.log` in the format: `[DROP] IP=<client_ip> Payload=<base64_encoded_header_value>`.
   - If the request is safe, it should pass the headers via `stdin` to the `/app/traffic_inspector` binary, capture its `stdout` output, and return that output to the client with a `200 OK` HTTP response.
4. **Run the Service**: Leave your compiled proxy running in the background listening on `127.0.0.1:8080` and `127.0.0.1:8443`.

The automated verification system will connect to your proxy on ports 8080 and 8443, send benign traffic (which must be processed by the binary and returned), and send the malicious open redirect payload (which must be blocked and logged).