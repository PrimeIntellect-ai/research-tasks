You are acting as a network security engineer responding to a suspected data exfiltration incident. Our Intrusion Detection System (IDS) flagged anomalous traffic, but the exact mechanism is hidden in custom HTTP headers. 

We captured an image of the IDS alert panel which specifies the target header being exploited. The image is located at `/app/alert_screenshot.png`. Use an OCR tool (like `tesseract`, which is preinstalled) to analyze this image and find the exact HTTP header name being used for exfiltration.

**Your Objective:**
Develop a Python-based traffic sanitizer that inspects HTTP request dumps, identifies malicious exfiltration payloads, and redacts them. 

The attackers are exfiltrating compiled Linux binaries (ELF files) by base64-encoding them and hiding them inside the specific HTTP header identified in the screenshot. 

1. Write a Python script at `/home/user/traffic_sanitizer.py`. It must be executable (`chmod +x`).
2. The script must accept exactly two positional arguments: an input JSON file path and an output JSON file path.
   Usage: `/home/user/traffic_sanitizer.py <input.json> <output.json>`
3. The input JSON files represent HTTP requests. They have a structure like:
   ```json
   {
     "method": "POST",
     "url": "/api/v1/status",
     "headers": {
       "Host": "example.com",
       "X-Something": "value"
     },
     "body": ""
   }
   ```
4. Your script must read the input JSON. If the target header (identified from the image) is present, it must decode its base64 content. 
5. If the decoded content is a valid ELF binary (starts with the ELF magic bytes `\x7FELF`), your script must redact the malicious payload by replacing the base64 string in the header value with the exact string `[REDACTED_ELF]`.
6. If the header does not contain an ELF binary (e.g., it's valid benign base64 data, or malformed), or if the header is absent, the JSON must remain absolutely unchanged.
7. Write the resulting JSON to the output file path. Ensure the JSON formatting and other headers remain intact.

You can test your script against the traffic dumps located in `/app/traffic_dumps/`. However, an automated grading system will run your script against a hidden set of clean and malicious traffic captures to verify its accuracy. Your script must perfectly preserve benign traffic and perfectly redact malicious traffic.