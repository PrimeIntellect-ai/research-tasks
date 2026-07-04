You are a DevOps engineer debugging a critical failure in our voice-alert log ingestion pipeline. 

The pipeline receives automated voice alerts, transcripts them, and sends payloads to a Go-based ingestion service. Currently, the service is crashing under load, dropping payloads due to encoding errors, and we have a strange statistical anomaly in our frontend logs.

Your task consists of four stages:

1. **Audio Decoding (Fixture)**
We received an automated incident alert via a legacy telephone system. The audio file is located at `/app/alert_log.wav`. It contains a sequence of DTMF (Dual-tone multi-frequency) dial tones representing the secret numeric Incident ID. You must decode this audio to recover the numeric Incident ID. (You may use tools like `ffmpeg`, `sox`, or write a script to decode the tones).

2. **Statistical Anomaly Investigation**
Examine the frontend access logs at `/app/requests.log`. These are JSON-formatted logs containing `user_id`, `endpoint`, and `status`. There is a statistical anomaly: one specific `user_id` is experiencing a disproportionately high number of HTTP 500 errors compared to others. Identify this `user_id` and write the exact numeric ID to `/home/user/anomaly_user.txt`.

3. **Concurrency and Serialization Debugging (Go)**
The backend ingestion service code is located in `/app/ingest/`. It is written in Go.
There are two major bugs you need to fix:
- A race condition causing intermittent crashes when multiple requests are processed concurrently (the state is tracked in a global map without synchronization).
- A serialization bug: the service is currently using standard Base64 encoding to decode payloads, but the new clients are sending Base64URL encoded strings (RFC 4648). Modify the code to correctly decode Base64URL payloads.

4. **Service Integration**
Once fixed, compile and run the Go ingestion service. 
- It must listen for HTTP traffic on `127.0.0.1:9000`.
- The endpoint `/ingest` must accept `POST` requests with JSON payloads like `{"user_id": 123, "payload": "base64url_string_here"}`.
- It MUST enforce authentication. It should check for the `Authorization` header. The expected format is `Authorization: Bearer <IncidentID>`, where `<IncidentID>` is the numeric sequence you extracted from the `/app/alert_log.wav` DTMF tones. Reject requests with missing or invalid tokens with an HTTP 401.

Leave the fixed service running in the background. Our automated verification system will issue requests to `127.0.0.1:9000/ingest` using the correct protocol, payloads, and authentication token to verify your fixes.