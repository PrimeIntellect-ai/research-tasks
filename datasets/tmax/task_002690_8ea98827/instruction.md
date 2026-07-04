You are tasked with securing a legacy, undocumented Go API binary that is known to be vulnerable to JWT signature bypass attacks (specifically, accepting tokens where the header specifies `"alg": "none"`). The source code for this binary has been lost, but it is located at `/app/legacy_api`.

Your objective is to deploy this binary in an isolated manner and write a secure reverse proxy in Go to protect it.

**Step 1: Intelligence Gathering**
1. Analyze the ELF binary `/app/legacy_api` (using tools like `strings` or `objdump`) to determine the hardcoded local port it listens on.
2. We have a scanned image of a sticky note left by the original developer at `/app/sticky_note.png`. Use an OCR tool (like `tesseract`, which is installed) to extract the static admin bypass key written on it.

**Step 2: The Secure Proxy**
Write a Go reverse proxy (save the source to `/app/proxy.go` and run it) that meets the following requirements:
1. It must listen on `127.0.0.1:8080` (HTTP).
2. It must intercept all incoming requests and inspect the `Authorization: Bearer <token>` header.
3. **Authentication & Validation:** The proxy must parse the JWT. 
   - If the token's header specifies `"alg": "none"` (case-insensitive) or is unsigned, the proxy **must** reject the request with a `401 Unauthorized` status code.
   - Valid tokens for this proxy will use the `HS256` algorithm and must be signed with the secret key: `proxy-secret-2024`.
4. **Forwarding:** If the token is valid and uses the correct algorithm, the proxy must forward the request to the `legacy_api` backend port discovered in Step 1.
5. **Backend Auth:** When forwarding to the backend, the proxy must inject an HTTP header `X-Admin-Key` containing the exact key value recovered from the sticky note image.
6. **Logging:** Any request blocked due to an invalid or `"alg": "none"` token must be logged to `/app/blocked_reqs.log`. This log file must be created with strict permissions (`0600`), and contain the text "Blocked JWT attempt".

**Step 3: Execution**
Ensure both the `/app/legacy_api` binary and your compiled Go proxy are running in the background. The automated verifier will send test requests to `127.0.0.1:8080` to ensure attacks are blocked and legitimate traffic is forwarded.