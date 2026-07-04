We are porting an older numerical analysis backend to a minimal container environment. The original tool was built as a CMake project and acted as a WebSocket worker, but we are encountering intractable shared library linkage errors (specifically with `libgmp.so` and `libjansson.so`) when deploying its binary to our new, minimal base image. 

To bypass these build system and dependency issues entirely, we want to rewrite the core numerical evaluator in pure Bash.

You have been provided with the original, stripped compiled binary at `/app/legacy_math`. Although we cannot deploy it in production, it functions perfectly in your current environment and can be used as a reference. 

Your task is to reverse-engineer the behavior of `/app/legacy_math` and write a Bash script at `/home/user/math_port.sh` that perfectly replicates its input/output behavior.

Here is what we know about the binary:
1. It reads a serialized JSON payload from standard input. The format is `{"query": {"value": <N>}}`, where `<N>` is a strictly positive integer.
2. It executes a specific iterative numerical algorithm on `<N>` until the value reaches 1. 
3. It outputs a serialized JSON payload to standard output representing the result.
4. It exits with code 0 on success.

Investigate the binary by sending it test inputs to determine the mathematical sequence it computes (it's a well-known sequence) and the exact structure of its JSON output. 

Once you understand the algorithm and serialization format, write `/home/user/math_port.sh` so that it parses the exact same JSON structure from standard input, computes the correct numerical result, and prints the identical JSON structure to standard output. 

Requirements:
- Your script must be written in Bash. You may use standard Unix utilities (like `jq`, `awk`, `sed`) available in the environment.
- Do not use WebSockets in your script; we are only porting the standard I/O evaluator.
- Ensure your script is executable (`chmod +x /home/user/math_port.sh`).
- Your script must produce bit-exact equivalent standard output as `/app/legacy_math` for any valid input integer between 1 and 100,000.