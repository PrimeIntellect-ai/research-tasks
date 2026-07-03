You are a penetration tester analyzing a recently compromised web server. The attacker used a visual side-channel to exfiltrate an encryption key, which was captured by a compromised surveillance camera as a video file. They then used this key to encrypt the web access logs to cover their tracks.

Your task consists of three phases:

**Phase 1: Key Extraction**
Analyze the video file located at `/app/intercepted.mp4`. The video consists of exactly 128 frames (at 10 frames per second). Each frame is entirely either pure black or pure white. 
- A black frame represents a binary `0`.
- A white frame represents a binary `1`.
Extract the bits in chronological order (frame 1 to 128) to form a 128-bit binary string. Convert this binary string into a 16-byte raw byte sequence. This is the AES-128 encryption key.

**Phase 2: Log Decryption**
Use the extracted 16-byte key to decrypt the file `/app/traffic.log.enc`. The file was encrypted using AES-128 in ECB mode with PKCS7 padding. 
The decrypted output will be a plain text file where each line is a JSON object representing an HTTP request. The JSON objects contain fields such as `request_id`, `headers`, `method`, and `path`.

**Phase 3: Threat Detection Script**
Write a Python script at `/home/user/detector.py` that can parse the decrypted log format and detect malicious requests. 
A request is considered **malicious** if it meets ANY of the following criteria:
1. The `Cookie` header contains a key `session_data` whose base64-decoded value contains the exact substring `admin=true`.
2. The HTTP `path` contains a directory traversal attempt (the exact substring `../` after URL decoding).
3. The `X-Forwarded-For` header contains shell metacharacters: any of `;`, `|`, or `$`.

Your script `/home/user/detector.py` must take exactly one argument (the path to a log file) and print the `request_id` of every malicious request, one per line, to standard output. 

*Note: Your script will be tested against a held-out test log to calculate its F1 score. You do not need to save the decrypted log anywhere specific, but your detector script must be robust and correctly implement the logic.*