You are an operations engineer triaging a critical incident. A containerized C microservice, `telemetry_parser`, has crashed in production. The system automatically gathered the source code and the resulting core dump, but the original executable and the temporary data file it was reading have been deleted by the container cleanup routine.

You have been provided with the following files in `/home/user/incident/`:
- `telemetry_parser.c` (The source code of the service)
- `build.sh` (The build script used to compile the service)
- `core` (The core dump from the crash)

Your tasks are:
1. **Fix the build**: The provided `build.sh` fails to compile the source code due to a compilation/linker error. Fix `build.sh` so that it successfully compiles `telemetry_parser.c` into an executable named `telemetry_parser` in the same directory.
2. **Analyze the Core Dump**: Using the newly compiled binary and the provided `core` dump, perform post-mortem debugging to determine the root cause of the crash. The crash was caused by a malformed telemetry packet.
3. **Extract the Malicious Payload Details**: Find the specific `device_id` (a string) and `payload_length` (an integer) of the telemetry packet that triggered the segmentation fault.
4. **Create a Post-Mortem Report**: Write these details into a log file at `/home/user/postmortem.txt`.

The format of `/home/user/postmortem.txt` must be exactly:
```
DeviceID: <extracted_device_id_string>
Length: <extracted_payload_length_integer>
```

Replace the bracketed placeholders with the exact values extracted from the crash state. Do not include any other text in the postmortem file.