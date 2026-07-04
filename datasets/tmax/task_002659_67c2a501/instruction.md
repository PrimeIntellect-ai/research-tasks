You are a mobile build engineer maintaining the CI/CD pipelines for a large mobile application. Recently, our pipeline has suffered from instability due to malformed build manifests, concurrent execution bugs, and failing UI automation tests. 

Your objective is to stabilize the pipeline by completing the following workflow:

**Phase 1: Video Automation Analysis & C++ Repair**
Our UI automation suite records test runs, but the frame analyzer tool crashes unpredictably. 
1. You are provided a test recording at `/app/test_run.mp4`.
2. Extract the frames using `ffmpeg` (e.g., at 1 fps).
3. The source code for the legacy frame analyzer is located at `/home/user/tools/analyzer/main.cpp`. It reads an image and outputs a state. However, it currently has a memory safety bug (Undefined Behavior/buffer overflow) preventing it from processing certain frames.
4. Fix the C++ memory safety issue and recompile the tool.
5. Run the fixed tool on the extracted frames from `/app/test_run.mp4`. Identify the exact frame number where the UI shows the error state (the analyzer will output `STATE=UI_ERROR_MODAL`).
6. Write the integer frame number to `/home/user/error_frame.txt`.

**Phase 2: Concurrency Pipeline Fix**
Our concurrent build dispatcher, written in Go, is dropping logs under heavy load.
1. Inspect `/home/user/dispatcher/main.go`.
2. It processes build jobs using goroutines and collects results into a shared slice, but suffers from a race condition.
3. Fix the Go concurrency pattern (e.g., using a Mutex or channels) so that `go test -race` passes and all results are reliably recorded.

**Phase 3: Manifest Validator (Rust)**
We are migrating our build manifests from Schema V1 to V2, and malicious or malformed configurations (e.g., path traversals in asset paths, invalid schema types) are breaking the macOS build nodes.
1. Create a Rust package at `/home/user/manifest_validator`.
2. Implement a CLI tool in Rust that takes a file path as its first argument: `target/release/manifest_validator <path_to_json>`
3. The tool must parse the JSON manifest and validate it. 
    - It must **accept** structurally valid V1/V2 JSON manifests that safely reference local assets.
    - It must **reject** (exit with a non-zero code) manifests that contain path traversal attempts in their `asset_path` fields (e.g., paths containing `../` or absolute paths pointing to `/etc/` or `/var/`), or invalid schemas (mixing V1 arrays with V2 objects).
4. Compile your solution using `cargo build --release`. 
5. We will test your binary against our hidden corpora.

Ensure all your code is compiled, dependencies are properly managed, and the exact files requested (`/home/user/error_frame.txt` and `/home/user/manifest_validator/target/release/manifest_validator`) exist.