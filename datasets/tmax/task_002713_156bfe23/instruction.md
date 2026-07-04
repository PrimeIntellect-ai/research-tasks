You are a DevSecOps engineer tasked with enforcing policy-as-code for a microservice that handles file uploads. The service is susceptible to path traversal and XSS attacks, and its authentication mechanism needs strict enforcement. 

To complete this task, you must create a Python-based request validator that acts as a security filter. 

**Step 1: Extract the Security Policy**
A whiteboard photo of the latest security policy has been saved at `/app/policy_spec.png`. 
You need to extract the information from this image (e.g., using `tesseract`). The image contains two critical pieces of information you will need for your script:
1. The custom HTTP Header name required for authentication.
2. The HS256 Secret Key used to sign the JWT tokens.

**Step 2: Implement the Policy Validator**
Create a Python script at `/home/user/policy_validator.py`. The script must accept a single command-line argument: the path to a JSON file representing an incoming HTTP request. 

The JSON files have the following schema:
```json
{
  "headers": {
    "User-Agent": "Mozilla/5.0...",
    "X-Your-Extracted-Header-Name": "Bearer <jwt_token>"
  },
  "upload_filename": "example.pdf",
  "upload_path": "/var/data/uploads/documents/"
}
```

Your script must evaluate the request and print EXACTLY the word `ALLOW` (if safe and authenticated) or `BLOCK` (if it violates any policy). It must exit with code 0.

The security policy rules are:
1. **Authentication (Token Validation):** The request must contain the custom header specified in the image. It must contain a valid JWT (format: `Bearer <token>`). The JWT must be signed with the exact Secret Key from the image using the HS256 algorithm. The token payload must contain the claim `"role": "uploader"`.
2. **Path Traversal Prevention:** The `upload_path` must NOT contain path traversal sequences. You must block requests where `upload_path` contains `../` or its URL-encoded equivalent `%2e%2e%2f` (case-insensitive).
3. **XSS / Injection Prevention:** The `upload_filename` must NOT contain the substrings `<script>` or `onload=` (case-insensitive).

**Step 3: Test Against the Corpora**
We have provided two directories containing sample JSON request dumps:
* `/app/corpus/clean/`: Contains perfectly legitimate requests that MUST be evaluated as `ALLOW`.
* `/app/corpus/evil/`: Contains malicious requests (invalid signatures, forged roles, path traversals, XSS payloads) that MUST be evaluated as `BLOCK`.

You should iteratively test your script against these corpora until it perfectly classifies all files. An automated verifier will test your script against these exact directories. 

Ensure your final script requires no dependencies other than standard Python libraries and `PyJWT` (you may install `PyJWT` via pip).