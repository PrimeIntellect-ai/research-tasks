You are tasked with implementing a critical telemetry processing service in Python to replace a legacy system. A multi-file Rust project was previously handling this, but it currently fails to compile due to missing dependencies, and the team has decided to migrate the backend service to Python using gRPC.

However, the specific Error-Correcting Code (ECC) and checksum algorithm used by the legacy system is poorly documented. We have recovered a stripped binary from the old system located at `/app/legacy_encoder`. This binary takes a raw string as an argument and outputs the hex-encoded version of the packet (which includes the data, a custom checksum, and parity bits for error correction). 

Your objectives are:
1. **Protobuf Definition**: Create a protobuf file `/home/user/telemetry.proto` with the following definition:
    - Package: `telemetry`
    - Service: `TelemetryProcessor`
    - RPC: `ProcessData` taking `DataPacket` and returning `ProcessResponse`
    - `DataPacket` message: contains a single field `bytes payload = 1;`
    - `ProcessResponse` message: contains `bool success = 1;` and `bytes decoded_data = 2;`

2. **Reverse Engineer ECC**: Analyze or treat `/app/legacy_encoder` as a black-box oracle to deduce its encoding scheme. The scheme involves a standard CRC32 checksum (with a specific initialization vector or XOR) and a simple custom bit-level parity/Hamming code. You must write Python code to decode and correct single-bit errors from this format.

3. **gRPC Server**: Implement the Python gRPC server in `/home/user/server.py`. 
    - The server must listen on `127.0.0.1:50051`.
    - When `ProcessData` is called, it should decode the payload, correct any single-bit errors, verify the checksum, and return `success=True` with the `decoded_data` if valid. If uncorrectable or checksum fails, return `success=False`.
    - Set up a test fixture or mock in your script to ensure your decoding logic matches the legacy binary's output.

4. Start the server in the background so it is running on `127.0.0.1:50051` when you complete the task.

Ensure the server is running and handles incoming gRPC requests correctly.