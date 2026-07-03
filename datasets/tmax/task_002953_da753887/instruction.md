As a release manager preparing for a new deployment, you need to automate the aggregation of gRPC protocol buffer updates. Over time, updates to the company's core service have been distributed as patch files.

Your workspace is located at `/home/user/release`. Inside, you will find:
- `base.proto`: The initial version `1.0.0` of the gRPC service definition.
- `manifest.txt`: A configuration file mapping version numbers to patch files. Each line is formatted as `VERSION=PATCH_FILE`.
- `patches/`: A directory containing the patch files referenced in the manifest.

Your goal is to write a Bash script at `/home/user/release/build.sh` that automates the release preparation. The script must accept a single argument: the target semantic version to build (e.g., `./build.sh 1.10.0`).

When executed, your script must perform the following actions:
1. **Semantic Version Filtering & Sorting:** Read `manifest.txt`. Filter for versions that are strictly greater than `1.0.0` and less than or equal to the target version provided as the argument. Sort these filtered versions in ascending Semantic Versioning order (e.g., `1.2.0` comes before `1.10.0`). You must implement or use a bash-compatible semantic version comparison (standard bash sort might not handle complex semver perfectly without specific flags or logic).
2. **Patch Processing:** Copy `base.proto` to a new file named `final.proto`. Iterate through the sorted versions and apply their corresponding patch files sequentially to `final.proto`. 
3. **Log the State Machine Transitions:** As you apply each patch, write the exact patch file path (as it appears in the manifest) to `/home/user/release/applied_patches.log`, one per line, in the order they were applied.
4. **Dependency Management & Code Generation:** 
   - Create a Python virtual environment at `/home/user/release/venv`.
   - Install the `grpcio-tools` package into this virtual environment.
   - Create an output directory `/home/user/release/out`.
   - Use the installed `grpc_tools.protoc` to compile `final.proto`, generating the Python gRPC stubs (`_pb2.py` and `_pb2_grpc.py`) inside `/home/user/release/out`.

**Constraints:**
- Execute your script for the target version `2.0.0` (i.e., run `/home/user/release/build.sh 2.0.0` to complete the task).
- Assume standard SemVer (MAJOR.MINOR.PATCH).
- Do not use root privileges. 
- You may use any standard Linux tools available to write your script (e.g., `patch`, `sort`, `awk`, `sed`).

Verify your success by ensuring `applied_patches.log` has the correct sequence and `/home/user/release/out/final_pb2.py` exists and is valid.