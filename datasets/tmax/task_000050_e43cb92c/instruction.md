You are a network security engineer investigating a series of attacks on a file upload service. The service is suspected to be vulnerable to path traversal. The attacker has been sending obfuscated payloads to bypass simple intrusion detection rules.

We have captured the network traffic of the incident, but due to a misconfiguration in our logging pipeline, the traffic log was encoded into a video file via an experimental optical data diode. 

Your tasks are as follows:

1. **Video Decoding**: The video file is located at `/app/traffic_pulses.mp4`. The video encodes a binary stream where each frame represents a single bit (measured at the center pixel). A white frame (brightness > 127) represents a `1` and a black frame (brightness <= 127) represents a `0`. The bits are grouped into 8-bit bytes (big-endian) to form ASCII characters. 
2. **Payload Extraction**: The resulting ASCII string is a JSON array of objects. Each object has an `id` (integer) and an `encoded_payload` (hex string).
3. **Vulnerability Analysis & Intrusion Detection**: Decode the `encoded_payload` (hex decoded, then base64 decoded) to reveal a JSON object representing the file upload request. Analyze the `filename` field for path traversal attempts. The attacker uses various encoding techniques (like URL encoding, double URL encoding) to hide `../` sequences. Flag any request that resolves to a path traversal attempt as malicious.
4. **Reporting**: Write your detections to a JSON file at `/home/user/results.json`. The format must be a dictionary mapping the string representation of the `id` to an integer (`1` for malicious, `0` for benign). Example:
```json
{
  "1": 0,
  "2": 1,
  "3": 0
}
```

Your final output will be evaluated against our hidden ground truth based on classification accuracy. You must achieve an accuracy of at least 0.95.