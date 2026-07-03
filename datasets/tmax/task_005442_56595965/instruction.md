You are tasked with fixing a broken Rust and C FFI project and creating a reliable Bash wrapper script for it.

The project is located at `/home/user/rust_evaluator`. It is designed to parse arithmetic expressions and evaluate them using a custom Abstract Syntax Tree (AST) data structure passed between Rust and C. However, the project currently fails to compile due to build system configuration errors and missing cross-compilation linking steps.

The previous developer left an audio voice note about the build requirements before they left. The audio file is located at `/app/dev_note.wav`. You should use a transcription tool (like `whisper.cpp`, which is available on the system as `whisper-cli`) to decode the audio and figure out the exact missing compiler flags, target architecture, and linking requirements.

Your goals are:
1. Transcribe the audio file `/app/dev_note.wav` to find the missing build system details.
2. Fix the compilation pipeline. You may modify the Rust code, C code, or create/modify Bash build scripts in `/home/user/rust_evaluator` as needed so that it successfully compiles.
3. Create a primary executable Bash wrapper at `/home/user/evaluate.sh`. This script must:
   - Take exactly one argument: a string containing an arithmetic expression (e.g., "4 + 5 * 2").
   - Pass this expression to the compiled Rust project.
   - Print *only* the final evaluated numerical result to standard output.
   - Automatically compile the Rust project on the first run if it hasn't been built yet.

The test system will programmatically evaluate your `/home/user/evaluate.sh` script against an adversarial fuzzer, comparing its output to a hidden reference implementation. It must match exactly.