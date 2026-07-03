You are acting as a release manager preparing deployments for a polyglot microservices project. 

Our deployment manifest was corrupted during transmission and is now stored as a Base64-encoded file containing UTF-16LE text. We need a Python script to decode this manifest, parse its contents into a custom dependency graph structure, and generate a bash shell script that builds the components in the correct topological order.

Your task:
1. Write a Python script at `/home/user/orchestrate.py`.
2. The script must read `/home/user/manifest.b64`.
3. Decode the Base64 content, then decode the resulting bytes as UTF-16LE.
4. The decoded text contains blocks defining components, formatted exactly like this:
   ```
   [Component: backend-go]
   Language: Go
   Path: /home/user/src/go-backend
   Deps: none

   [Component: cli-rust]
   Language: Rust
   Path: /home/user/src/rust-cli
   Deps: backend-go
   ```
   (Dependencies are comma-separated. "none" means no dependencies).
5. Parse this text into a custom Python data structure representing a Directed Acyclic Graph (DAG) of the build dependencies.
6. Perform a topological sort on your DAG to determine the correct build order. If A depends on B, B must be built before A. Ties can be resolved alphabetically by component name.
7. Generate a bash script at `/home/user/build_all.sh` (make sure to set it as executable, e.g., `chmod +x`). For each component in the sorted order, the bash script should contain exactly these two lines:
   ```bash
   echo "Building <Component Name>..."
   cd <Path> && make build
   ```
8. The very first line of `/home/user/build_all.sh` must be `#!/bin/bash`.

When you are done, run your script so that `/home/user/build_all.sh` is generated and ready for the automated test to execute and verify.