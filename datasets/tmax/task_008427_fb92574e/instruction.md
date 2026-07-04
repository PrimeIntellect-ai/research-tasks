You are a penetration tester analyzing a custom web server for vulnerabilities. You have been provided with an access log at `/home/user/server.log`. 

Your objective is to identify an open redirect vulnerability, perform a known-plaintext attack to recover a secret encryption key used for session tokens, and implement a sandboxed parser to safely analyze potentially malicious log entries.

**Step 1: Pattern Matching & Open Redirect Detection**
Parse `/home/user/server.log`. The log follows this format:
`[TIMESTAMP] IP METHOD PATH_AND_QUERY SESSION_TOKEN`
Identify the IP address that successfully exploited an open redirect. An open redirect in this system occurs when the `redirect` query parameter points to an external domain (starts with `http://` or `https://` instead of a relative path like `/dashboard`), AND the HTTP status (if we had one, but just look for the external URL) indicates a successful login. 
Find the `SESSION_TOKEN` associated with the user `admin` (the log line right after the attacker's IP tested the open redirect usually contains the admin logging in, or you can find the admin's encrypted token). Actually, extract ALL `SESSION_TOKEN`s from the logs.

**Step 2: Cryptanalysis (Known-Plaintext Attack)**
The `SESSION_TOKEN` is a hex-encoded string. Once decoded to bytes, it is encrypted using a repeating-key XOR cipher.
You know the exact plaintext format for session tokens: `USER:<username>;ROLE:<role>;TS:<10-digit-timestamp>`
For example, the guest user token plaintext looks exactly like: `USER:guest;ROLE:guest;TS:1700000000`
Find a guest token in the logs (the log line will mention "guest login"), use the known plaintext format and the timestamp in the log to derive the repeating XOR key.
Once you have the key, decrypt the `SESSION_TOKEN` of the `admin` user to find their exact 10-digit timestamp.

**Step 3: Process Isolation / Sandboxing**
Some of the query parameters in the log are intentionally crafted by an attacker to cause a Regular Expression Denial of Service (ReDoS). 
Write a Python script that evaluates a specific vulnerable regex `(a+)+b` against the query parameters of every log line. Because this can hang forever, you MUST execute the regex search inside a separate child process (e.g., using `multiprocessing`) and use the `resource` module (`resource.setrlimit`) to sandbox the process by setting `RLIMIT_CPU` to 1 second. 
Identify the query parameter string that triggers the CPU timeout.

**Expected Output**
Create a file at `/home/user/report.json` with the following structure:
```json
{
  "attacker_ip": "1.2.3.4",
  "xor_key": "string_value_of_the_recovered_key",
  "admin_timestamp": "10_digit_timestamp_string",
  "redos_payload": "the_exact_query_string_that_timed_out"
}
```