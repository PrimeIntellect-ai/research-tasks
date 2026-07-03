You are a systems programmer debugging a C-based dependency resolver (`/home/user/system_builder`) that uses a Rust parser backend. The project currently fails to build, link, and validate inputs correctly. Your goal is to fix the pipeline, ensure the library is correctly linked, and build a robust input validator.

Here are the specific issues you must resolve:

1. **Audio Transcription for Graph Rules**:
   A key configuration file was corrupted, but a voice memo detailing the missing dependency edges was saved at `/app/sys_audio.wav`. Use a transcription tool (like Whisper or ffmpeg + speech recognition available in the environment) to transcribe it. Write the exact missing edges described in the audio into `/home/user/system_builder/missing_edges.txt` (one edge per line, formatted as `NODE_A->NODE_B`).

2. **Rust Backend Fix**:
   The C application delegates string encoding validation to a Rust library in `/home/user/system_builder/rust_backend`. However, the Rust code currently fails to compile due to an ownership and borrow-checker issue in `src/lib.rs`. Fix the Rust code so it compiles successfully into a dynamic library (`librust_backend.so`) while maintaining its intended FFI signature. 

3. **C Linking and Build System**:
   The C executable fails to link correctly because of improper library ordering in the `Makefile` (similar to initialization failures in CI due to module import ordering). Modify the `Makefile` so that the C application statically/dynamically links against `librust_backend` and the native `libgraph_utils` in the correct dependency order. The build command `make all` must produce a working binary named `dep_resolver`.

4. **Adversarial Corpus Validation (Graph Traversal & Encoding)**:
   You must implement the `validate_file(const char* filepath)` function inside `main.c`. This function must:
   - Call the fixed Rust FFI function to verify the file contents are strictly valid ASCII and custom safe characters (rejecting malformed or malicious encodings).
   - Parse the file into a directed graph and perform a traversal to check for cyclic dependencies.
   - Combine the parsed file edges with the rules from `missing_edges.txt`.
   
   The binary `./dep_resolver <filepath>` must return an exit code of `0` if the file has valid encoding AND contains no cycles. It must return `1` (or another non-zero exit code) if it has invalid encoding OR contains a dependency cycle.

   Two corpora are provided to test your solution:
   - `/app/corpus/clean/`: Contains 100 valid, acyclic dependency files with proper encoding.
   - `/app/corpus/evil/`: Contains 100 adversarial files that either contain subtle dependency cycles or malicious character encodings designed to bypass naive checks.

To complete this task, your compiled `./dep_resolver` must correctly accept 100% of the clean corpus and reject 100% of the evil corpus. Once you have finished the implementation, write a summary log to `/home/user/system_builder/validation_results.log` detailing how many evil and clean files your binary successfully handled.