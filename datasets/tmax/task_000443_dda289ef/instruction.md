You are a DevSecOps engineer tasked with digitizing and enforcing an old legacy security policy. 

Your organization recently acquired an application, and its Web Application Firewall (WAF) policy was only provided as a scanned image document. You need to implement this policy as code to evaluate a historical dataset of web traffic.

**Inputs provided:**
1. `/app/policy_scan.png` - An image of the security policy matrix. You will need to use OCR (e.g., Tesseract) or vision tools to extract the exact WAF rules. The policy defines rules regarding:
   - XSS/Injection blocking in URIs
   - Certificate validation requirements
   - HTTP Header length limits
   - Cookie security flag requirements
2. `/app/traffic_dataset.jsonl` - A JSON Lines file containing historical request metadata. Each line is a JSON object with the following schema:
   - `id`: string, unique identifier
   - `uri`: string, requested path and query
   - `headers`: dictionary of HTTP headers
   - `set_cookie`: string or null, the value of the Set-Cookie header if present
   - `cert_metadata`: dictionary containing `issuer` (string) and `depth` (integer), or null if HTTP.

**Your Goal:**
1. Read the policies from the image.
2. Write a Python script at `/home/user/policy_enforcer.py` that processes `/app/traffic_dataset.jsonl` and applies the extracted WAF rules.
3. The script must output its decisions to `/home/user/decisions.jsonl`. 
   Each line must be a valid JSON object with exact keys: `{"id": "<request_id>", "action": "<ALLOW or BLOCK>"}`.
   If a request violates *any* of the rules found in the image, the action must be "BLOCK". Otherwise, it is "ALLOW".

Your script must be fully automated. The automated verification system will run your generated `decisions.jsonl` against a hidden ground-truth file to compute the accuracy of your WAF implementation.