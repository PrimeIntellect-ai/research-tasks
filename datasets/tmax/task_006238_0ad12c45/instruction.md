You are a network security engineer inspecting traffic for a web application. The application has a file upload handler that is supposed to strictly isolate uploaded files into a sandbox directory (`/home/user/app/uploads/`). However, we suspect an attacker has bypassed this isolation using a path traversal vulnerability to drop an XSS payload elsewhere on the server.

I have provided a JSON log of intercepted HTTP requests in `/home/user/traffic.json`. 

Your task is to:
1. Write a Python script at `/home/user/extract.py` that parses the `/home/user/traffic.json` file.
2. Identify the single HTTP POST request that attempts to exploit a path traversal vulnerability in the filename parameter to escape the upload sandbox.
3. Extract the exact contents of the XSS payload (the body of the malicious request) and save it to `/home/user/extracted_payload.txt`.
4. Extract the malicious filename path used to perform the traversal and save it to `/home/user/target_path.txt`.

The JSON file contains a list of dictionaries, where each dictionary represents a request with keys: `method`, `endpoint`, `headers` (which is a dictionary), and `body`. The filename is specified within the `Content-Disposition` header.

Do not include any extra whitespace or newlines in your output files beyond what is extracted.