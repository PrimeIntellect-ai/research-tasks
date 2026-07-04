You are a QA engineer tasked with setting up an automated test environment for a legacy IoT embedded system. The actual hardware is scarce, so we need to test our firmware integration using a software emulator exposed over gRPC.

Your objective is to build a gRPC test server that acts as an interpreter for a custom binary firmware bytecode, and a client script that sends a test payload to verify the emulator.

**Step 1: Protobuf Definition**
Create a protobuf file at `/home/user/emulator.proto` with the following specification:
- `syntax = "proto3";`
- `package iot_test;`
- A service named `Emulator`
- An RPC named `ExecuteFirmware` that takes a `FirmwareRequest` and returns a `FirmwareResponse`.
- `FirmwareRequest` must contain a single field: `bytes bytecode = 1;`
- `FirmwareResponse` must contain a single field: `repeated int32 readings = 1;`

**Step 2: The Emulator Server**
Create a Python script at `/home/user/server.py` that compiles the protobuf (you may need to install `grpcio` and `grpcio-tools`), implements the `Emulator` service, and listens on port `50051`.

The `ExecuteFirmware` method must implement a virtual machine/interpreter for the following custom 8-bit bytecode instruction set. The emulator maintains a single integer register `temp` (initialized to 0).
- `0x01` (SET_TEMP): Takes a 1-byte payload (signed 8-bit integer). Sets `temp` to this value.
- `0x02` (ADD_TEMP): Takes a 1-byte payload (signed 8-bit integer). Adds this value to `temp`.
- `0x03` (READ_TEMP): Takes no payload. Appends the current value of `temp` to the response `readings`.
- `0x04` (END): Takes no payload. Immediately halts execution and returns the response. Any bytes following this opcode should be ignored.

*Request Validation Requirements:*
- The emulator must validate the incoming payload. If the `bytecode` length exceeds 128 bytes, immediately abort the RPC with `grpc.StatusCode.INVALID_ARGUMENT` and the detail message `"Payload too large"`.
- If an unknown opcode is encountered during execution, abort the RPC with `grpc.StatusCode.INVALID_ARGUMENT` and the detail message `"Invalid opcode"`.

**Step 3: The Test Client**
Create a Python script at `/home/user/client.py`. This script must:
1. Read the binary bytecode payload from `/home/user/test_payload.bin`. (Assume this file already exists).
2. Connect to the gRPC server at `localhost:50051`.
3. Call `ExecuteFirmware` with the bytecode.
4. Extract the `readings` list from the response.
5. Serialize the list as a JSON array and write it to `/home/user/test_results.json`.

**Execution**
Once your scripts are written, start the server in the background, run the client script to process `/home/user/test_payload.bin`, and ensure `/home/user/test_results.json` is generated successfully.