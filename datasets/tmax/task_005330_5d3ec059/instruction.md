You are a DevSecOps engineer tasked with enforcing security policies for a file upload service. The service recently started accepting Base64-encoded filenames in its JSON API to bypass special character issues, but we suspect attackers are exploiting this to perform path traversal attacks.

You have two objectives:

**Objective 1: Incident Detection**
We have exported recent upload logs to `/home/user/upload_logs.json`. The file contains a list of JSON objects, each with a `request_id` and an `encoded_filename` (which is a Base64-encoded string). 
Write a Python script to decode the filenames and detect any malicious requests. A filename is considered malicious if, after Base64 decoding, it contains the exact string `../` or `..\`.
Extract the `request_id` of all malicious requests and save them to `/home/user/flagged_requests.txt`. The file should contain one integer ID per line, sorted in ascending numerical order.

**Objective 2: Policy Verification Payload**
To integrate a new policy check into our CI/CD pipeline, we need a baseline exploit payload.
Create a JSON file at `/home/user/exploit_payload.json` that perfectly mimics a request attempting to access the system password file. 
The JSON file must have exactly two keys:
1. `"request_id"`: set to the integer `9999`
2. `"encoded_filename"`: set to the Base64-encoded value of the string `../../../etc/passwd`

Ensure all output files are placed exactly at the specified absolute paths.