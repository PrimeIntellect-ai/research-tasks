You are an automation specialist tasked with building a robust data processing pipeline to decode legacy telemetry streams. 

We have a sample video feed located at `/app/telemetry_feed.mp4` which contains a burnt-in diagnostic overlay. First, analyze the video frame at exactly `00:00:05` (frame 150 at 30fps). Extract the 4-byte hexadecimal sequence displayed in the bottom-right corner. You will use this sequence as the XOR decryption key for the primary pipeline.

Next, develop a Python CLI application at `/home/user/pipeline_decoder.py` that processes raw binary telemetry data from `stdin` and writes JSON results to `stdout`.

The incoming binary stream consists of multiple consecutive frames with the following structure:
1. **Magic Bytes (2 bytes):** `0xFE 0xED`
2. **Encoding Flag (1 byte):** 
   - `0x01` indicates the payload is encoded in `CP1252`.
   - `0x02` indicates `Shift-JIS`.
   - `0x03` indicates `UTF-8`.
3. **Payload Length (2 bytes, Big Endian):** Specifies the length `L` of the encrypted payload.
4. **Encrypted Payload (L bytes):** The text data, encrypted via repeating-key XOR using the 4-byte hex key extracted from the video.
5. **Checksum (1 byte):** The XOR sum of all bytes in the unencrypted payload.

Your script must perform the following:
- Read the stream continuously until EOF.
- Validate constraints: If the magic bytes are incorrect, or if the calculated checksum of the decrypted payload does not match the checksum byte, silently drop the frame and append a single line `{"status": "error", "reason": "constraint_violation"}` to `/home/user/pipeline.log`.
- Character Encoding: Decrypt the payload and decode it using the specified character set. If decoding fails due to invalid characters, drop the frame and log `{"status": "error", "reason": "encoding_fault"}` to `/home/user/pipeline.log`.
- For valid frames, output a JSON line to `stdout`: `{"status": "success", "length": L, "payload": "DECODED_STRING"}`.

Ensure your Python script is executable (`chmod +x`). It must process arbitrary amounts of binary data efficiently and strictly adhere to the output formatting, as it will be rigorously tested against millions of fuzzed inputs to ensure bit-exact output equivalence with our legacy specification.