You are a mobile build engineer maintaining our SDK release pipelines. We need a tool that mathematically calculates the "breaking impact score" of changes between different versions of our API protobuf definitions. 

Your task is to create a Rust-based gRPC service that compares two semantic versions of our proto files, generates a unified diff, and calculates an impact score based on a mathematical formula.

Here is the specification:

1. **Protobuf Files Location:**
   Our historical API definitions are located in `/home/user/protos/`. You will find directories named after semantic versions (e.g., `1.0.0`, `1.1.0`, `2.0.0`), each containing an `api.proto` file.

2. **The gRPC Service:**
   Create a new Rust project at `/home/user/build_tools/impact_analyzer`.
   Implement a gRPC server in Rust (using `tonic` and `prost`) listening on `127.0.0.1:50051`.
   The service definition must be strictly this:
   ```protobuf
   syntax = "proto3";
   package impact;

   service ImpactService {
       rpc CalculateImpact (ImpactRequest) returns (ImpactResponse);
   }

   message ImpactRequest {
       string v1 = 1;
       string v2 = 2;
   }

   message ImpactResponse {
       int32 score = 1;
   }
   ```

3. **Service Logic (CalculateImpact):**
   - Parse `v1` and `v2` as Semantic Versions (SemVer). 
   - Compare them: if `v1` is greater than or equal to `v2`, the service must return a gRPC `InvalidArgument` error.
   - Read `/home/user/protos/<v1>/api.proto` and `/home/user/protos/<v2>/api.proto`. If either file doesn't exist, return a `NotFound` error.
   - Execute a unified diff between the two files using the system `diff` command: `diff -U0 <file1> <file2>`.
   - Parse the unified diff output. Let `A` be the number of added lines (lines starting with `+` but strictly not `+++`). Let `D` be the number of deleted lines (lines starting with `-` but strictly not `---`).
   - Calculate the mathematical impact score using this formula: `Score = (D * D * 3) + A`.
   - Return the calculated score.

4. **Integration Script:**
   Write a bash script at `/home/user/test_harness.sh` that:
   - Compiles and starts your Rust gRPC server in the background.
   - Waits for the server to be ready on port `50051`.
   - Uses `grpcurl -plaintext -d '{"v1": "1.0.0", "v2": "1.1.0"}' 127.0.0.1:50051 impact.ImpactService/CalculateImpact` to get the score, and appends the raw JSON output to `/home/user/report.log`.
   - Uses `grpcurl -plaintext -d '{"v1": "1.1.0", "v2": "2.0.0"}' 127.0.0.1:50051 impact.ImpactService/CalculateImpact` and appends the raw JSON output to `/home/user/report.log`.
   - Kills the background gRPC server before exiting.

Ensure your code is robust, compiles correctly, and `/home/user/test_harness.sh` is executable. You may install `grpcurl` or use any standard Rust crates you need via `cargo`.