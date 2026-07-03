You are a DevSecOps engineer tasked with enforcing security policies as code. A rogue microservice has been deployed locally by a development team. It is known to use weak cryptographic secrets for its authentication tokens.

Your objective is to write and execute a Python script that audits this service, cracks its secret, and proves the vulnerability by accessing a protected endpoint.

Here are the specific requirements:
1. **Service Discovery:** The microservice is listening on a local port somewhere between `9000` and `9010` (inclusive).
2. **Token Extraction:** The service has an unprotected endpoint at `/guest_token` that returns a JSON response containing a JWT (JSON Web Token) in the format `{"token": "<jwt_string>"}`.
3. **Password Cracking:** The JWT is signed using the `HS256` algorithm. The secret key is a weak dictionary word. A list of possible passwords is provided in `/home/user/weak_passwords.txt`. You must crack the JWT secret offline.
4. **Token Generation:** Once cracked, forge a new JWT signed with the discovered secret. The payload must be exact: `{"user": "auditor", "role": "admin"}`.
5. **Secure Access:** Send a GET request to the `/secure_data` endpoint of the microservice. You must include the forged token in the HTTP headers as `Authorization: Bearer <your_forged_token>`.
6. **Reporting:** Extract the raw plaintext response from the `/secure_data` endpoint and save it to `/home/user/audit_result.txt`.

You may install any necessary Python libraries (like `requests` or `PyJWT`) using `pip`. 

Ensure your final output is exactly the plaintext flag returned by the `/secure_data` endpoint, written to `/home/user/audit_result.txt` with no additional formatting or whitespace.