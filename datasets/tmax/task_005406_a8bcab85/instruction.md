You are a build engineer managing a continuous integration pipeline for a microservices architecture. Your team uses compiled C++ and Go binaries as gRPC plugins. Recently, the pipeline was compromised, and malicious/malformed artifacts were injected into the build cache.

Your objective is to write a Python-based artifact classifier that analyzes and filters out bad binaries. 

You are provided with:
1. `/app/plugin.proto`: The protobuf definition for the plugin service, which defines a `PluginService` with a single RPC `CheckHealth(HealthRequest) returns (HealthResponse)`.
2. `/app/reference_plugin`: A stripped, packed reference implementation of a known-good plugin. It takes one command-line argument (the port to listen on).

You must write a classification script at `/home/user/classifier.py`. The script will be invoked as:
`python3 /home/user/classifier.py <path_to_binary_artifact>`

The script must exit with code `0` if the artifact is safe (clean), and exit with code `1` if the artifact is malicious or malformed (evil).

To classify an artifact as **evil**, it must detect ANY of the following:
1. **Architecture mismatch:** The binary is not a valid 64-bit x86-64 ELF executable (requires structured data parsing of ELF headers).
2. **Malicious Payload (Assembly-level analysis):** Disassembling the `.text` section reveals an attempt to call the `execve` syscall directly. You must detect the x86-64 assembly pattern for this (setting `rax` or `eax` to `0x3b` or `59` immediately followed by a `syscall` instruction within a few lines).
3. **Performance/Reliability Benchmark:** When the binary is executed as a background process (e.g., `./binary 50051`), it must successfully bind to the port, accept a gRPC `CheckHealth` call, and respond within 100 milliseconds. If it hangs, crashes, or takes longer than 100ms, it is evil.

Requirements:
- You must compile the protobuf file for Python usage.
- You must manage the lifecycle of the binary under test (start it, wait for it to be ready, test it, and forcefully terminate it).
- Ensure your script cleans up any spawned processes before exiting.
- Use only standard standard libraries and `grpcio-tools`, `grpcio` (which you may install via pip). Do not use advanced reverse-engineering Python wrappers; rely on standard CLI tools like `readelf` and `objdump` via subprocesses.

Write your script robustly to handle missing files or premature crashes.