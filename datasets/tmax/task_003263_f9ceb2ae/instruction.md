You are a security engineer tasked with taking over and securing a legacy authentication service, rotating its compromised credentials, and building a high-performance auditing tool to verify the new security posture.

The previous engineer left abruptly, leaving only a picture of a sticky note containing the legacy master credentials and base port.

Your objectives:

1. **Extract Legacy Credentials**: Analyze the image located at `/app/legacy_creds.png`. It contains the legacy master password and a base port number.
2. **Service Auditing & Discovery**: The authentication service is running on a port somewhere between the base port and base port + 1000. Write a script to quickly scan this range and identify the port responding to a basic HTTP GET request at `/health` with the header `X-Legacy-Ping: ping`.
3. **Authentication Flow & Credential Rotation**: 
   - Once you find the port, initiate a credential rotation by sending a POST request to `/rotate`. 
   - You must include a JSON body with `{"legacy_password": "<PASSWORD_FROM_IMAGE>"}`.
   - The service will respond with a new, highly secure rotation token. Save this token exactly as received into `/home/user/new_token.txt`.
4. **Content Security Policy Enforcement**: The service relies on a configuration file at `/app/service_config.json`. Modify this file to include a restrictive CSP policy. Add a key `"csp": "default-src 'self'; script-src 'none'; object-src 'none';"` to the JSON root.
5. **High-Performance Privilege Auditing**: The new security policy requires that we can rapidly audit authentication tokens across distributed endpoints. Write a highly optimized Python script at `/home/user/fast_audit.py` that reads the token from `/home/user/new_token.txt` and sends 5,000 asynchronous or concurrent POST requests to the local service at `/audit` (using the same port you discovered). Each request must include the header `Authorization: Bearer <NEW_TOKEN>`. 
   - Your script must output the number of successful (HTTP 200) responses.
   - *Performance matters:* To pass the security pipeline, your script must be heavily optimized (e.g., using `asyncio` and `aiohttp`) to complete all 5,000 requests within a strict time limit.

Ensure your code is clean and saves the required outputs in the exact locations specified.