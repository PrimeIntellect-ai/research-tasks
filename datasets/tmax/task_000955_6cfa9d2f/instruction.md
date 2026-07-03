You are acting as a security engineer tasked with rotating credentials and fixing a severe vulnerability in our internal webhook system, located in `/home/user/app`.

Currently, the webhook client (`/home/user/app/client.py`) is analogous to a JWT implementation accepting `algorithm=none`: it entirely bypasses TLS/SSL certificate chain validation by setting `verify=False` when making requests to the server. Furthermore, the server (`/home/user/app/server.py`) is using an expired certificate and lacks a strict Content Security Policy (CSP).

I need you to perform the following credential rotation and security hardening steps:

1. **Rotate Server Certificates:** 
   Modify `/home/user/app/server.py` so that the Flask application uses the newly generated certificates `/home/user/certs/new_server.crt` and `/home/user/certs/new_server.key` instead of the old ones.

2. **Enforce Certificate Chain Validation:**
   Modify `/home/user/app/client.py` to strictly validate the server's certificate against the new Certificate Authority (CA). Change the insecure request to use the CA bundle located at `/home/user/certs/new_ca.pem`.

3. **Implement Content Security Policy:**
   Update the Flask endpoint in `/home/user/app/server.py` to include the following HTTP response header exactly:
   `Content-Security-Policy: default-src 'none'; frame-ancestors 'none';`

4. **Verify the Fix:**
   Start the server in the background, wait 2 seconds for it to bind, and then run `python3 /home/user/app/client.py`. 
   The `client.py` script is already written to print the response headers and body as a JSON string. Redirect the standard output of `client.py` to `/home/user/result.log`.

Do not change the port (8443) or the route (`/webhook`) in the server or client. Ensure `result.log` is successfully created with the strict CSP header present and that the connection succeeds using the validated TLS chain.