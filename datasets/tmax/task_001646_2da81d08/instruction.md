You are a build engineer responsible for recovering and serving a legacy build pipeline. A previous system crash lost the exact sequence of patches required to build our core C++ analytics library, but we managed to salvage a diagnostic video of the CI pipeline UI.

Your task consists of four main phases:

**Phase 1: Video Artifact Recovery**
There is a video file located at `/app/ci_diagnostic.mp4`. This video displays a sequence of textual dependency declarations flashing on screen. Each declaration is in the format `Node_A depends on Node_B`. 
Extract the frames from this video (you may use `ffmpeg` and tools like `tesseract-ocr` or `grep` on raw text strings embedded in the video if applicable, but note that the text is cleanly rendered in black and white). 
Reconstruct the full directed acyclic graph (DAG) of dependencies.

**Phase 2: Patch Processing and Resolution**
In `/home/user/patches/`, you will find several `.patch` files named after the nodes in the graph (e.g., `Node_A.patch`). 
Using the DAG you extracted, determine the correct topological sort order (from leaf dependencies up to the root) and apply these patches sequentially to the base C++ codebase located in `/home/user/legacy_lib/`. Keep a log of the applied patch order in `/home/user/patch_order.txt` (one patch filename per line).

**Phase 3: C++ Memory Safety Repair**
After applying the patches, the C++ codebase in `/home/user/legacy_lib/` will compile, but running the tests (`make test`) will fail due to memory leaks and a buffer overflow introduced by the patches. 
Diagnose and repair the C++ code so that it compiles cleanly, passes all tests, and runs without undefined behavior (Valgrind is installed to help verify this). 

**Phase 4: Rust API Service**
Create a Rust project in `/home/user/build_service/`. Write a Rust HTTP server that binds strictly to `127.0.0.1:8080` and exposes the following endpoints:
1. `GET /graph`: Returns a JSON array of strings representing the topologically sorted list of applied patches (e.g., `["Node_C.patch", "Node_B.patch", "Node_A.patch"]`).
2. `POST /verify`: Executes the compiled C++ binary `/home/user/legacy_lib/analytics_engine` and returns its standard output. The request must include an `Authorization` header with the exact token `Bearer artifact-token-992`.

Start your Rust server in the background and ensure it stays running. Leave the server running on port 8080 before you indicate completion.