You are an operations engineer triaging a production incident. Our core data processing component, a stripped C++ binary located at `/app/telemetry_processor`, has been crashing (segfaults, unhandled exceptions) or hanging in infinite loops when processing certain malformed telemetry payload files.

Since we cannot currently patch the binary, your task is to write a standalone C++ sanitiser that acts as a gatekeeper. The sanitiser must inspect incoming telemetry files and reject any payload that would cause the processor to crash, hang, or fail, while allowing all valid payloads through.

**Format details we've gathered:**
The telemetry files follow a custom binary format:
1. **Magic Header:** 4 bytes, ASCII "TLVM".
2. **Checksum:** A 32-bit unsigned integer (little-endian). The checksum formula is: the sum of all remaining bytes in the file, multiplied by 31 (modulo 2^32).
3. **Payload:** A sequence of TLV (Type-Length-Value) records:
   - **Type:** 1 byte
   - **Length:** 2 bytes (unsigned little-endian)
   - **Value:** `Length` bytes of arbitrary data

**Your objective:**
1. Investigate how `/app/telemetry_processor` behaves when given various crafted inputs. Identify the specific record types, length edge-cases, or structural flaws that trigger crashes or infinite loops in the processor.
2. Write a C++ program at `/home/user/sanitiser.cpp`.
3. Compile it to `/home/user/sanitiser` (e.g., `g++ -O2 /home/user/sanitiser.cpp -o /home/user/sanitiser`).
4. The sanitiser must take a single command-line argument: the path to a telemetry file to check.
   - Example invocation: `/home/user/sanitiser ./test_payload.bin`
5. If the file is perfectly valid and can be safely processed by `/app/telemetry_processor`, the sanitiser must exit with code **0**.
6. If the file has an invalid checksum, an invalid header, or contains any structural anomalies/records that would cause the processor to crash or hang, the sanitiser must exit with code **1**.

You are free to write scripts or generate test files to fuzz or test the binary to discover its vulnerabilities. A successful solution will correctly identify and reject 100% of a hidden adversarial corpus of malicious files, while accepting 100% of a clean corpus.