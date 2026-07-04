You are an incident responder investigating a potential breach on a web server. We suspect an attacker exploited a path traversal vulnerability in a file upload API endpoint. 

You have been provided with a web server log file located at `/home/user/upload_access.log`. 

The log file contains entries in the following format:
`[TIMESTAMP] IP_ADDRESS METHOD /api/upload?target=[ENCODED_PATH] HTTP/1.1 STATUS_CODE`

The `target` parameter is Base64 encoded.

Your tasks are:
1. Write a Python script to parse `/home/user/upload_access.log`.
2. Find all successful upload requests (HTTP status code `200`).
3. Decode the Base64 `target` parameter for these successful requests.
4. Identify which of the successful requests are path traversal attacks (i.e., the decoded path contains the pattern `../`).
5. Extract the decoded malicious paths and save them, one per line, to a file named `/home/user/malicious_paths.txt`. Sort the lines alphabetically.
6. To help our red team verify the patch later, craft a new payload. Write a Python script to generate the Base64 encoded string for the exact path `../../../../home/user/proof.txt`. Save the resulting Base64 string to a file named `/home/user/test_payload.txt`.

Ensure your Python scripts use standard libraries only. All files should be placed in `/home/user/`.