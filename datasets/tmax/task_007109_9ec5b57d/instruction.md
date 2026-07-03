You are acting as a penetration tester conducting a targeted vulnerability assessment on a local API service. 

We suspect the API's JWT authentication implementation is vulnerable to the "alg: none" attack, where the server accepts tokens without a cryptographic signature if the algorithm header is set to "none".

The target API server code is located at `/home/user/api_server.go`. 
First, start this server in the background. It will bind to `localhost:8080`.

Your objective is to exploit this vulnerability, extract sensitive data, and write a Go tool to process and redact the data safely.

Write a Go program located at `/home/user/exploit.go` that performs the following steps:
1. **Token Generation (Exploit):** Craft a raw JWT with the header `{"alg": "none", "typ": "JWT"}` and the payload `{"username": "admin", "role": "admin"}`. Remember that a JWT consists of three base64url-encoded parts separated by dots (`header.payload.signature`). For an "alg: none" token, the signature part should be empty, but the trailing dot must remain.
2. **Automated Extraction:** Use this forged token in the `Authorization: Bearer <token>` header to send a GET request to `http://localhost:8080/api/users`. 
3. **Sensitive Data Redaction:** The endpoint will return a JSON array of user records. Each record contains `id`, `name`, `email`, and `credit_card` fields. Your Go program must parse this JSON, and securely redact the `credit_card` field for every user. The redaction rule is: replace all digits except the last 4 with asterisks (`*`). For a 16-digit card, the format must be `************1234`.
4. **Save Output:** Write the resulting redacted JSON array to `/home/user/redacted_dump.json` with pretty-printing (indentation of 2 spaces).

Requirements:
- Ensure your Go program handles base64url encoding correctly (without padding).
- Do not use any external third-party JWT libraries; construct the token manually in your Go code using standard libraries to demonstrate the exploit mechanics.
- Run your Go program to produce the `/home/user/redacted_dump.json` file.