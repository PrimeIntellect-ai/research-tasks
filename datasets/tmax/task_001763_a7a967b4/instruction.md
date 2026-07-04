You are an open-source maintainer reviewing a broken PR for a mathematical signal processing tool. A contributor attempted to migrate our gRPC service schema to v2, add integration tests, and implement the new mathematical processing logic in Bash, but they abandoned the PR in a broken state.

The original feature request was reported via an audio memo from our lead researcher. You will find this voicemail at `/app/issue_42.wav`. You need to transcribe this audio to understand the exact schema additions and the mathematical operation required for the v2 migration.

Here is your task:
1. **Transcribe the Audio**: Listen to (transcribe) `/app/issue_42.wav` using available tools (e.g., `whisper` or `ffmpeg` + python speech recognition) to determine the requested fields for the new gRPC schema and the exact mathematical formula.
2. **Schema Migration**: Update the broken protobuf schema located at `/home/user/math_service/proto/service.proto`. Ensure it correctly defines the `ProcessRequest` and `ProcessResponse` messages as described in the audio.
3. **Implement the Logic**: Fix the Bash script `/home/user/math_service/process.sh`. This script is meant to act as our standalone processing core before we wire it into the gRPC C++ server. It must read a JSON representation of the `ProcessRequest` from standard input, perform the exact mathematical transformation specified in the audio memo on the array, and output a JSON representation of the `ProcessResponse` to standard output. 
4. **Unit/Integration Testing**: Make sure your `process.sh` is robust. It should perfectly replicate the mathematical transformation on any valid sequence of integers. 

**Requirements for `process.sh`:**
- Must be written in Bash (you may use tools like `jq`, `awk`, or `bc`).
- Must read from `stdin`. Input format: `{"data": [int, int, ...], "multiplier": int, "shift": int}` (field names must match the ones you discover in the audio).
- Must print to `stdout`. Output format: `{"result": [int, int, ...]}`.
- Make sure `process.sh` is executable.

The automated test will evaluate your `/home/user/math_service/process.sh` by generating thousands of random input sequences and asserting that its output exactly matches our reference implementation.