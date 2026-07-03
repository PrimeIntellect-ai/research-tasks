You are a developer tasked with fixing a multi-file gRPC/Rust project's build pipeline. The project uses a custom Bash orchestrator to package protobuf definitions and calculate an integrity checksum before the Rust compilation step.

The build script `package.sh` runs perfectly on the original author's local machine but fails randomly in the CI environment due to an unpredictable file processing order and a character encoding issue with the generated checksum.

Your task:
1. Investigate and fix `/home/user/grpc-math-service/package.sh`.
   - The script currently uses `find` to concatenate all `.proto` files into a `bundle.proto` file, but the concatenation order depends on the filesystem. Modify it so the files are concatenated in strict alphabetical order based on their filenames.
   - The script calculates a SHA256 checksum of the bundled file, extracts the hex string, and encodes it in Base64. However, it currently includes a trailing newline in the Base64 output, which breaks the Rust `build.rs` parser. Fix the Base64 encoding so it outputs purely the encoded string without any newlines.

2. Create an end-to-end test orchestrator script at `/home/user/test_orchestrator.sh`.
   - The script must be executable.
   - It should create a mock test fixture directory at `/home/user/mock_protos/`.
   - Inside this directory, create two protobuf files:
     - `a_math.proto` with the exact content: `syntax = "proto3"; message AddRequest { int32 a = 1; int32 b = 2; }`
     - `b_math.proto` with the exact content: `syntax = "proto3"; message SubRequest { int32 a = 1; int32 b = 2; }`
   - The orchestrator should then execute `/home/user/grpc-math-service/package.sh` passing `/home/user/mock_protos` as the target directory (the script takes the directory as its first argument).
   - Finally, the orchestrator must read the generated `manifest_hash.txt` and write "PASS" to `/home/user/test_result.log` if the base64 checksum strictly matches the expected output, or "FAIL" otherwise. (You will need to manually determine the expected base64 checksum for the concatenated, sorted mock files to hardcode the check in your orchestrator).

Ensure you fix the script and run your orchestrator to generate the `/home/user/test_result.log` file.