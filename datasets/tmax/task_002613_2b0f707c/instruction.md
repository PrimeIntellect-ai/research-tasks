We are migrating our internal data processing pipeline, but the previous developer left the codebase in a completely disorganized state and only left a voice memo detailing the encoding specification. 

Locally, the developer's test scripts were passing because they hardcoded absolute paths and compiled everything directly without proper linking, but it fails in CI due to missing headers, bad include ordering, and ABI mismatches between C++ objects.

Your objectives:
1. **Understand the Specification:** Listen to the voice memo located at `/app/spec_memo.wav`. You will need to transcribe it (e.g., using a Python script with `openai-whisper` or any tool you can install). This memo contains the exact rules for our custom character encoding and checksum algorithm.
2. **Organize the Project:** You will find the disorganized files in `/app/legacy_project/`. Move them into a structured directory under `/home/user/project/` with standard `src/`, `include/`, and `bin/` directories.
3. **Shared Library & ABI:** The encoding logic must be implemented in C++ but exposed via a strict C ABI. Create a shared library `libencoder.so`. The function signature must be `void encode_data(const char* input, char* output);` (assume `output` buffer is sufficiently large).
4. **CLI Tool:** Write a C++ command-line tool `encoder_cli` that links against `libencoder.so`. It must read standard input line-by-line (until EOF), pass each line to the `encode_data` function, and print the resulting encoded string to standard output, one per line.
5. **Build System:** Write a `Makefile` in `/home/user/project/` that compiles the shared library and the CLI tool, placing the final executable at `/home/user/project/bin/encoder_cli`.

Ensure that the CLI executable behaves exactly according to the rules in the audio memo, as it will be rigorously tested against a reference implementation with thousands of randomized inputs.