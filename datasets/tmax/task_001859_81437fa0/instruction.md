You are an incident responder investigating a recent breach. The attacker compromised a web service and left behind a steganographic video artifact and a trail of HTTP requests. 

Your task is to analyze the video to recover the cryptographic secret, then build a Python tool that classifies captured HTTP requests as benign or malicious based on authentication and payload analysis.

**Step 1: Artifact Analysis (Video)**
The attacker left a video file at `/app/evidence.mp4` (Resolution: 1280x720, 30 FPS). 
Through preliminary intelligence, we know the attacker hid the 16-character HMAC secret key used for signing authentication tokens in the first 16 frames of this video.
Specifically, the Red (R) color channel of the exact center pixel `(x=640, y=360)` in frames 0 through 15 represents the ASCII integer value of the characters of the secret key in sequence (e.g., Frame 0's Red value is the 1st character's ASCII code, Frame 1's Red value is the 2nd, etc.).
Extract this secret key. You may use `ffmpeg`, `Python`, or any tools you install to extract and analyze the frames.

**Step 2: HTTP Request Classifier**
The attacker used this secret to forge JSON Web Tokens (JWTs) and sent malicious payloads. We have captured numerous raw HTTP requests.
Create a Python script at `/home/user/detector.py` that takes a single file path as a command-line argument. The script must parse the raw HTTP request in that file and classify it.

An HTTP request is classified as **EVIL** if ANY of the following conditions are met:
1.  **Invalid Signature:** The request has an `Authorization: Bearer <token>` header, but the JWT signature is invalid when verified against the extracted 16-character secret key using the `HS256` algorithm.
2.  **Privilege Escalation:** The JWT signature is valid, but the decoded token payload contains the claim `"admin": true`.
3.  **Exploit Payload:** The HTTP `User-Agent` header contains the exact substring `${jndi:` (indicative of a Log4Shell attempt).

If none of these conditions are met, and the token is valid, the request is classified as **CLEAN**.

**Execution Requirements:**
Your script `/home/user/detector.py` will be invoked by an automated grading system like this:
`python3 /home/user/detector.py <path_to_raw_http_file.txt>`

*   If the request is **CLEAN**, the script MUST exit with status code `0`.
*   If the request is **EVIL**, the script MUST exit with status code `1`.
*   The script should cleanly handle standard raw HTTP/1.1 formatting.
*   You are free to use `pip install` to install libraries such as `PyJWT` or `Pillow` if needed.

Ensure your script is robust and perfectly matches the criteria above. The grading suite will test your script against a hidden corpus of clean and evil requests.