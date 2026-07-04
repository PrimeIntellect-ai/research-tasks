As an edge computing engineer, you are tasked with fixing and deploying a telemetry collection system for our new IoT devices. The setup involves fixing a broken vendored package, configuring a simulated mount point, and writing a robust parser for the sensor data.

Perform the following steps:

1. **Fix the IoT Sender Package**
   We have vendored a connectivity and sending package at `/app/iot-sender-1.2.0`. It is supposed to read the `IOT_ENDPOINT` environment variable to determine where to send diagnostics. However, it currently fails to detect the endpoint even when the variable is set. Locate the bug in `/app/iot-sender-1.2.0/sender.py`, fix the typo or logic error preventing it from reading `IOT_ENDPOINT`, and ensure the package works.

2. **Configure Simulated fstab**
   Because you do not have root access on this edge node, the system reads a custom fstab file for user-mountable sensor drives. Create a file at `/home/user/device_fstab` containing exactly one line. This line must configure the mount for a block device with `UUID=1234-ABCD` to the mount point `/home/user/sensor_data` using the `ext4` filesystem. The mount options must be `defaults,ro,noauto,user`, and the dump and pass values must both be `0`.

3. **Write the Telemetry Parser**
   You need to write a robust Python script at `/home/user/parse_telemetry.py` to parse raw telemetry frames. Your script's output must perfectly match the behavior of our compiled reference binary located at `/app/telemetry_oracle`.
   
   The script must accept a single command-line argument: a hex string representing the sensor frame. It must print a single minified JSON object to standard output.
   
   **Frame Specification:**
   - **Byte 0:** Magic byte, must be `0x5A`.
   - **Byte 1:** Sensor ID (unsigned 8-bit integer).
   - **Byte 2:** Payload Length (`L`) (unsigned 8-bit integer).
   - **Bytes 3 to 3+L-1:** The payload data.
   - **Byte 3+L:** Checksum. The checksum is calculated as the bitwise XOR of all preceding bytes (Magic ^ Sensor ID ^ Length ^ Payload byte 0 ^ ... ^ Payload byte L-1).
   
   **Validation and Output Rules:**
   - If the input is not a valid even-length hex string, output: `{"error": "invalid_hex"}`
   - If the input byte sequence is too short to contain the header (3 bytes) plus a checksum (1 byte), or if the total length of the byte sequence does not exactly equal `3 + L + 1`, output: `{"error": "bad_length"}`
   - If the Magic byte is not `0x5A`, output: `{"error": "bad_magic"}`
   - If the Checksum does not match the calculated XOR value, output: `{"error": "bad_checksum"}`
   - If the frame is completely valid, output: `{"sensor_id": <int>, "payload_hex": "<lowercase_hex_string_of_payload>"}`
   
   Ensure your script handles exceptions gracefully and strictly adheres to this JSON schema.