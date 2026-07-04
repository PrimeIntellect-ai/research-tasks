You are tasked with building a core component for a new binary artifact manager. The component is a C program that parses a custom "Artifact Binary Container" (ABC) format, extracts metadata, verifies the payload, and outputs a structured JSON report.

**Stage 1: Fix the Vendored JSON Library**
We use `cJSON` for JSON generation. The source is vendored at `/app/cJSON`. However, a recent commit broke the build. 
1. Diagnose and fix the issue in `/app/cJSON` so that it compiles correctly into a shared library (`libcjson.so`).
2. Ensure you can link against it for your parser.

**Stage 2: The ABC Parser**
Write a C program at `/app/abc_parser.c` (compilable to `/app/abc_parser`) that takes a single file path as a command-line argument. 

The ABC format is structured as follows (all multi-byte integers are Little Endian):
1. **Magic Bytes**: 4 bytes, must be exactly `ARTF`.
2. **Version**: 1 byte, `uint8_t`, must be `1`.
3. **Flags**: 1 byte, `uint8_t`. If bit 0 is set (e.g., `flags & 1`), the payload is XOR-obfuscated.
4. **Metadata Length**: 2 bytes, `uint16_t`.
5. **Payload Length**: 4 bytes, `uint32_t`.
6. **Metadata**: A string of exactly *Metadata Length* bytes. It contains semicolon-separated key-value pairs (e.g., `arch:x86_64;os:linux;`). Keys and values are separated by a colon. 
7. **Payload**: Exactly *Payload Length* bytes of data.

Your program must:
1. Open the file and parse the header.
2. If the file cannot be read, or if the Magic Bytes or Version are incorrect, or if the file is truncated (ends before the metadata or payload are fully read), output EXACTLY `{"error": "invalid format"}` to `stdout` and exit with code `1`.
3. If valid, parse the metadata string into a JSON object.
4. Process the payload: if the XOR-obfuscated flag (bit 0) is set, deobfuscate the payload by XORing every byte with `0x5A`. Calculate the 8-bit sum (modulo 256) of the final (deobfuscated) payload bytes.
5. Print a JSON response to `stdout` using `cJSON` with the following structure (unformatted/minified is fine, but it must be valid JSON):
   ```json
   {
     "metadata": {
       "arch": "x86_64",
       "os": "linux"
     },
     "payload_size": 1024,
     "payload_checksum": 142
   }
   ```
6. Exit with code `0`.

Ensure your program handles missing semicolons, empty metadata, and large payloads robustly. An automated fuzzer will test your `/app/abc_parser` binary against a reference implementation for thousands of valid and maliciously malformed inputs to ensure bit-exact output equivalence.