You are an engineer working on a Web Security team. We need to deploy a custom, lightweight C-based middleware proxy that sits in front of our web backend. This proxy acts as a security filter that validates requests using a custom checksum mechanism before forwarding them.

Your task is to write and run this C proxy, along with a mock backend to test it.

**Step 1: The Mock Backend**
Write a Python script `/home/user/mock_backend.py` that starts an HTTP server on `127.0.0.1:9090`. 
- For any GET request, it should return a 200 OK status with the body `Authorized Backend Data\n`.
- Run this backend in the background.

**Step 2: The Security Proxy**
Write a C program at `/home/user/secure_proxy.c` and compile it to `/home/user/secure_proxy`. 
The proxy must:
1. Listen for incoming TCP connections on `127.0.0.1:8080`.
2. When a client connects, read the HTTP request. Implement a state machine to parse the HTTP Request-Line (e.g., `GET /some/path HTTP/1.1`) to extract the **URI** (e.g., `/some/path`), and parse the headers to find the custom header `X-Secure-Checksum: <value>`.
3. Compute the Adler-32 checksum of the **URI** string (excluding the protocol or query parameters, just the path part parsed from the Request-Line). 
   *(Use the standard Adler-32 algorithm: `A = 1`, `B = 0`. For each byte `c` in the URI, `A = (A + c) % 65521`, `B = (B + A) % 65521`. The checksum is `(B << 16) | A`.)*
4. Compare the computed checksum (represented as an unsigned 32-bit integer in decimal format) with the value provided in the `X-Secure-Checksum` header.
5. **If valid:** Forward the exact raw HTTP request to the Python backend at `127.0.0.1:9090`, read the response from the backend, and send it back to the client. Then log the following exact line to `/home/user/proxy.log`:
   `[ALLOW] <URI> <PROVIDED_CHECKSUM_VALUE>`
6. **If invalid or missing:** Do not forward the request. Send the client an `HTTP/1.1 403 Forbidden\r\n\r\n` response. Log the following to `/home/user/proxy.log`:
   `[DENY] <URI> <PROVIDED_CHECKSUM_VALUE>` (Use `NONE` if the header was missing).
7. Close the client connection after each request.

Start your compiled proxy in the background. Both servers must be running when you complete your task.

Make sure your C code handles socket creation, binding, listening, and basic memory management safely.