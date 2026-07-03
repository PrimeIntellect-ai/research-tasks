You are acting as a network security engineer investigating a recent incident. We suspect an attacker leveraged an open redirect vulnerability during a login flow, combined with a rogue TLS certificate, to steal user credentials.

We have provided you with several artifacts in the `/app/incident_data/` directory:
1. `capture_session.mp4`: A screen recording of a terminal session where an admin was monitoring traffic and logs during the attack.
2. `traffic.pcap`: The packet capture corresponding to the incident.
3. `auth_logger.elf`: A custom compiled Linux binary that was used to log authentication events.
4. `server_cert.pem` and `suspicious_cert.pem`: TLS certificates found on the server.

Your task is to analyze these artifacts and create a Python script at `/home/user/analyze_incident.py` that accomplishes the following:

1. **Video Analysis**: Use `ffmpeg` to extract frames from `capture_session.mp4`. Analyze the frames to identify the exact timestamps (down to the second) when the open redirect payload `GET /login?redirect=...` is visible on the screen.
2. **Binary Analysis**: Analyze `auth_logger.elf` to determine the static XOR key it uses to redact sensitive data before writing to its log files. You will need to reverse engineer the binary to find this key (it is a 4-byte key).
3. **Traffic & Cert Analysis**: Parse `traffic.pcap` and correlate the open redirect events found in the video with TLS handshakes. Determine which requests were served using the rogue `suspicious_cert.pem`.
4. **Integration**: Your script must output a JSON file at `/home/user/incident_report.json` containing a list of malicious events. Each event must include the timestamp, the unredacted payload (using the key found in step 2), and a boolean indicating if the rogue certificate was used.

The JSON format should be:
```json
[
  {
    "timestamp": "HH:MM:SS",
    "unredacted_payload": "string",
    "used_rogue_cert": true
  }
]
```

Your script `/home/user/analyze_incident.py` will be evaluated against a hidden ground truth dataset. The evaluation metric will be the F1 score of the identified malicious payloads and timestamps. You must achieve an F1 score >= 0.90 to pass. Ensure your script runs cleanly and generates the report without manual intervention.