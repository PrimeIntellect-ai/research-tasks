You are acting as a Release Manager preparing the deployment pipeline for a microservice architecture. The old architecture uses gRPC, and the new system is moving to a real-time WebSocket architecture. As part of this transition, we are doing a major schema migration where all integer-based IDs are being converted to UUID strings. 

Your task is to write a standalone Bash build and migration script at `/home/user/release_builder.sh`.

The initial state of the system contains a legacy Protocol Buffers definition:
`/home/user/src/protos/v1/user.proto`

Your script (`/home/user/release_builder.sh`) must perform the following actions when executed:

1. **Schema Migration:**
   - Create a new directory: `/home/user/src/protos/v2/`.
   - Read `/home/user/src/protos/v1/user.proto`.
   - Perform a text-based schema migration to generate `/home/user/src/protos/v2/user.proto` with the following rules:
     - Change the package declaration from `package v1;` to `package v2;`.
     - Find any message fields of type `int32` where the field name ends with `_id` and change the type to `string`. Do not modify other `int32` fields or other field names.
     - Preserve all field numbers and formatting as closely as possible.

2. **Build System Linking (Indexing):**
   - Create a text file at `/home/user/proto_index.txt`.
   - It should contain the absolute paths to all `.proto` files in the `/home/user/src/protos/` directory tree (both `v1` and `v2`), with one path per line.
   - The list must be sorted alphabetically.

3. **Test Fixture and Mock Setup (for WebSockets):**
   - To test the new WebSocket service, generate a mock data stream file at `/home/user/ws_mock_stream.jsonl` (JSON Lines format).
   - Generate exactly 3 lines (JSON objects) representing the new `User` message schema (v2).
   - Each JSON object must have the following keys and exact values for the 3 rows:
     - Row 1: `"user_id": "uuid-1"`, `"username": "alpha"`, `"group_id": "group-1"`, `"is_active": true`
     - Row 2: `"user_id": "uuid-2"`, `"username": "beta"`, `"group_id": "group-2"`, `"is_active": false`
     - Row 3: `"user_id": "uuid-3"`, `"username": "gamma"`, `"group_id": "group-3"`, `"is_active": true`
   - Ensure it is strictly formatted as valid NDJSON (Newline Delimited JSON).

Ensure your script is executable (`chmod +x`) and runs without errors. You should run your script to complete the deployment preparation. Once you verify the output files exist and are correct, your task is complete.