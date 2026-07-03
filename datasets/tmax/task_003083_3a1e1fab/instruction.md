You are an incident responder investigating a suspicious background service running on a Linux server. A local API runs on port 8080, and a background worker script is periodically authenticating against it. Security analysts suspect that the worker script is leaking its authentication payload via a classic system vulnerability involving process execution.

Your task is to investigate the running system, exploit the leakage to recover the credentials, verify the authentication flow, and document your findings.

Perform the following steps:
1. Identify the background process simulating the API client. It is periodically executing a command that passes a base64-encoded authentication token as a command-line argument. You must find this process and extract the leaked base64 token. (Hint: look closely at the process list and what is visible in the system's process filesystem).
2. Decode the extracted token.
3. Use the decoded token to authenticate against the local API at `http://localhost:8080/flag`. The API requires the token to be passed in the `Authorization: Bearer <decoded_token>` header.
4. Identify the standard CWE (Common Weakness Enumeration) identifier that corresponds to "Invocation of Process Using Visible Sensitive Information" (specifically, leaking sensitive data via command-line arguments).
5. Compile your findings into a strictly formatted JSON file at `/home/user/incident_report.json`.

The JSON file must have exactly this structure:
```json
{
  "leaked_token_encoded": "the_base64_string_you_found",
  "leaked_token_decoded": "the_decoded_plaintext_string",
  "cwe_id": "CWE-XXX",
  "retrieved_flag": "the_flag_returned_by_the_api"
}
```

Ensure that you do not kill the background processes, as you may need them to run to capture the leaked data. Use Bash and standard Linux tools to complete your investigation.