You are acting as a penetration tester analyzing logs from a recent security incident. We suspect an attacker was probing our server for an SSL parsing vulnerability by sending base64-encoded TLS certificates in the HTTP User-Agent header, which resulted in HTTP 500 Internal Server Error responses.

You have been provided with a web server access log at `/home/user/access.log`. 

Your task is to write a Python script at `/home/user/analyze.py` that does the following:
1. Parses `/home/user/access.log` (standard combined log format, but with a base64-encoded User-Agent).
2. Filters for log entries that resulted in an HTTP 500 status code.
3. Extracts the IP address and the base64-encoded User-Agent string from those lines.
4. Decodes the User-Agent string. 
5. The decoded string will be a PEM-formatted X.509 certificate. Parse this certificate (you may use the `cryptography` library, which is installed) and extract the Subject's Common Name (CN) attribute.
6. Write the results to a new file at `/home/user/extracted_cns.txt`. Each line in the file should correspond to a matched log entry and be formatted exactly as `IP: CN` (e.g., `192.168.1.50: attacker.com`).

Run your script to generate the `/home/user/extracted_cns.txt` file. Make sure your script handles standard Base64 decoding and correctly identifies the Subject Common Name from the PEM certificate.