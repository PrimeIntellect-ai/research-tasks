You are a network security engineer investigating a series of open redirect attacks and token manipulation attempts against your company's authentication service.

You have a local environment under `/app/` containing a multi-service stack:
1. An `nginx` reverse proxy (listening on port 8080)
2. A `flask` authentication service (listening on port 5000)
3. A `redis` session store (listening on port 6379)

Currently, the services are brought up by `/app/start.sh`, but the end-to-end authentication flow is broken. 

**Part 1: Service Composition**
Fix the nginx configuration located at `/app/nginx/nginx.conf`. The `/auth` endpoint on the nginx server (port 8080) is supposed to proxy requests to the flask application (port 5000). Currently, it returns a 502 or 404 because the `proxy_pass` directive is missing or incorrectly configured. Modify `/app/nginx/nginx.conf` so that `curl -I http://localhost:8080/auth?next=/dashboard` successfully reaches the flask app and returns a 302 redirect. Restart nginx after modifying it (`sudo nginx -s reload` or restart the script).

**Part 2: Token Validation & Open Redirect Detection (Adversarial Corpus)**
The auth service issues a session token that encodes a redirection URI. Attackers are manipulating this token to cause open redirects (e.g., redirecting users to `//evil.com` or `https://attacker.site`).

A token is a Base64-encoded string. Once decoded, it has the format:
`user_id|redirect_uri|signature`

You must write a C program at `/home/user/token_validator.c` and compile it to `/home/user/token_validator`.
We have provided a skeleton at `/home/user/token_validator.c` that already includes a `base64_decode` function. 

Your C program must read a Base64-encoded token from `stdin` and implement the following logic:
1. Decode the Base64 token.
2. Parse the decoded string to extract the `redirect_uri` and `signature`.
3. Validate the `signature`: It must be exactly 64 characters long (representing a SHA-256 hex digest). If not, reject the token.
4. Validate the `redirect_uri` to prevent open redirects:
   - A SAFE redirect must start with exactly one forward slash `/` (e.g., `/dashboard`, `/profile/settings`).
   - It MUST NOT start with two forward slashes `//` (protocol-relative URL bypass).
   - It MUST NOT start with a scheme like `http://` or `https://` or `javascript:`.
   - It MUST NOT contain control characters.

If the token is SAFE, your program must output exactly `VALID` to standard output and exit with code `0`.
If the token contains an open redirect payload or an invalid signature, your program must output exactly `INVALID` to standard output and exit with code `1`.

Your compiled tool will be tested automatically against a corpus of valid tokens and malicious tokens.