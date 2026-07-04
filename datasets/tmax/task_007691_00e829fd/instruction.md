Wake up! It's 3 AM and you're the on-call engineer. We just got paged because the legacy telemetry ingest pipeline is completely down. 

The downstream database is rejecting the incoming data, and the ingest service is repeatedly crashing with a serialization/encoding error.

Here is what we know:
1. Legacy C sensors are sending a binary payload saved temporarily at `/home/user/telemetry.bin`.
2. A Python script at `/home/user/parse_telemetry.py` is supposed to read this binary file, decode the sensor name, and extract a double-precision (8-byte) float value representing the critical telemetry reading.
3. The binary format specification from the legacy team states:
   - Byte 0: An unsigned 8-bit integer `N` representing the length of the sensor name in bytes.
   - Bytes 1 to `N`: The sensor name encoded as a UTF-8 string.
   - Bytes `N+1` to `N+8`: A big-endian double-precision float (8 bytes).

Currently, `parse_telemetry.py` is crashing with a `UnicodeDecodeError`, and even when the encoding error is bypassed, the extracted float value exhibits massive precision loss (showing garbage values). We suspect there is an off-by-one boundary error causing misalignment in both the string decoding and the float deserialization.

Your task:
1. Diagnose and fix the off-by-one and deserialization errors in `/home/user/parse_telemetry.py`.
2. Run the fixed script to parse `/home/user/telemetry.bin`.
3. Save the correctly extracted data to a log file at `/home/user/recovered.log`.

The format of `/home/user/recovered.log` must be exactly one line:
`Device: <sensor_name>, Value: <float_value>`

Example:
`Device: Sensor-X, Value: 42.1234`

Fix the script, recover the data, and save the log file so the downstream pipelines can recover.