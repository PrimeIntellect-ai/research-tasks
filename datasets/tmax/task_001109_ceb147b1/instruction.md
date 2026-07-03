You are a network engineer tasked with inspecting and sanitizing traffic in a legacy telemetry system. 

We have a system with two primary components running locally:
1. A telemetry producer that sends encoded sensor data.
2. A telemetry consumer (server) that receives and processes this data.

Recently, the consumer has been experiencing crashes due to malicious payloads being injected into the network. 

Your objectives:
1. Analyze the provided packet capture `/home/user/capture.pcap` and the producer's compiled logic in `/home/user/telemetry_lib.pyc` to reverse-engineer the custom payload encoding mechanism.
2. Identify the structure of the exploit payload. Analysis of the consumer core dumps reveals that the exploit triggers when a decoded payload contains the exact string `"CRASH_OVERRIDE_V1"`.
3. Write a Python proxy script at `/home/user/proxy.py` that:
   - Listens on `localhost:8000` (acting as the server to the producer).
   - Forwards sanitized traffic to the actual consumer on `localhost:8001`.
   - Decodes incoming payloads on-the-fly.
   - Drops any payload containing the exploit string `"CRASH_OVERRIDE_V1"`.
   - Re-encodes and forwards benign payloads to the consumer.

The telemetry system services are managed by a startup script. You must configure your proxy to run continuously and ensure the end-to-end flow is intact. 

When you are ready for verification, ensure your proxy is running on port 8000 and forwarding to 8001. Our automated testing suite will blast your proxy with a mix of benign and malicious payloads. Your proxy's performance will be graded based on the F1 score of successfully forwarded benign payloads versus correctly dropped malicious payloads.

Requirements:
- Your proxy must be written in Python and saved to `/home/user/proxy.py`.
- Ensure your proxy handles multiple consecutive connections gracefully.