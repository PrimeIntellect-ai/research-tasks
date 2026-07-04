You are a security engineer tasked with implementing a new Web Application Firewall (WAF) filter to handle a recent credential rotation and block malicious payloads. 

We have securely transmitted the newly rotated session token to you in a video file located at `/app/rotation_alert.mp4`. The video is 10 seconds long (1 fps). One of the frames contains a QR code that holds the new session token.

Your task has two parts:

**Part 1: Recover the Rotated Token**
Extract frames from `/app/rotation_alert.mp4` and decode the QR code (you may use `ffmpeg`, `pyzbar`, `Pillow`, or `cv2` as needed; install any required Python libraries via `pip`). The QR code contains a plain-text string which is the new active session token.

**Part 2: Build the WAF Detector**
Write a Python script at `/home/user/detector.py` that acts as a request classifier. It must take a single command-line argument: the path to a JSON file representing an incoming HTTP request. 

The JSON structure looks like this:
```json
{
  "method": "POST",
  "headers": {
    "Authorization": "Bearer <token>",
    "X-Encoded-Payload": "<base64_string>"
  },
  "cookies": {
    "session_id": "<token>"
  }
}
```

Your script must implement the following security checks:
1. **Credential Validation:** The request MUST contain the exact new session token (extracted from the video) in EITHER the `Authorization` header (after "Bearer ") OR the `session_id` cookie. If neither matches the new token, the request must be rejected.
2. **Payload Inspection:** If the `X-Encoded-Payload` header is present, you must base64-decode it. If the decoded payload contains any of the following strings (case-insensitive), the request must be rejected:
   - `drop table`
   - `1=1`
   - `<script>`

**Execution & Output:**
- If the request passes all checks (valid token AND no malicious payload), your script must exit with status code `0` (Accept).
- If the request fails any check, your script must exit with status code `1` (Reject).

Your solution will be tested against a hidden corpus of clean and malicious requests. Ensure `/home/user/detector.py` is robust and handles missing keys gracefully (rejecting gracefully if authentication is absent).