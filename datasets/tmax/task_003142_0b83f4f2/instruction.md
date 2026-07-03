You are an on-call engineer responding to a 3am page. The edge telemetry system is reporting aggregate anomalies in our financial trading sensors. The edge devices transmit high-precision JSON telemetry over UDP to a legacy ingestion pipeline, but the downstream database is showing corrupted or skewed values.

We suspect that a recent data transformation script introduced a precision loss bug for specific ranges of data, but we don't know which sensor is being affected.

Here is what we know:
1. A network packet capture of the incoming edge traffic has been saved to `/home/user/traffic.pcap`. The traffic consists of UDP packets sent to port 5000. The payload of each packet is a UTF-8 encoded JSON string followed by a newline.
2. The intermediate pipeline processes these JSON strings using the script at `/home/user/transform.py`.

Your task is to:
1. Extract the raw JSON payloads from the packet capture.
2. Pass the extracted raw JSON data through `/home/user/transform.py`.
3. Perform a data transformation diff analysis between the original JSON payloads (from the pcap) and the transformed JSON payloads.
4. Track down the precision loss: Identify the `sensor_id` where the absolute difference between the original `value` and the transformed `value` is strictly greater than `0.001`.
5. Write ONLY the exact string of the affected `sensor_id` to a file named `/home/user/faulty_sensor.txt`.

Ensure your final result is placed exactly in `/home/user/faulty_sensor.txt` so our automated systems can verify the fix and silence the pager.