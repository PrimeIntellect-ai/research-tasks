You are a security engineer tasked with rotating credentials for a legacy internal service. 

An old microservice is currently running locally on `http://127.0.0.1:8000`. We need to trigger the credential rotation endpoint at `POST /rotate_credentials`, but we have lost the original administrative access token. 

There are rumors that the service's custom JWT authentication middleware is vulnerable to the "alg=none" bypass. We know the following about the service's expected authentication format:
1. It expects a standard Bearer token in the `Authorization` HTTP header.
2. The payload must be a JWT containing the claims `{"user": "admin", "role": "superuser"}`.
3. If the vulnerability exists, the server will accept tokens with an unprotected signature if the algorithm is set to `none`.

Your task:
1. Craft a forged JWT in Python that exploits the `alg=none` vulnerability. Remember that JWT parts must be base64url-encoded.
2. Send a POST request to `http://127.0.0.1:8000/rotate_credentials` with your forged token in the `Authorization: Bearer <token>` header.
3. The successful response will be a JSON object containing the new credential.
4. Save the exact, unmodified JSON response returned by the server to `/home/user/rotation_result.json`.

Ensure your final file is valid JSON and strictly contains the server's response.