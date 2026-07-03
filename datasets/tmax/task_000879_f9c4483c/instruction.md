You are a QA engineer responsible for our CI/CD build environments. We have a hybrid project containing C++ (built with CMake) and Rust code. Recently, we've had issues with our build log parser missing critical errors or failing on adversarial log injection attempts. We also have a build failure where CMake cannot find a shared library during the linking phase.

Your tasks are:

1. **Log Parser Translation & Hardening**:
   We have an old, incomplete Python script (`/app/legacy_parser.py`) that parses our build logs using a basic state machine. You need to translate this into a pure Bash script named `/home/user/log_sanitizer.sh`.
   The script must take a single file path as an argument.
   It must output `CLEAN` to stdout and exit with code 0 if the log is valid and contains no severe errors or injection attempts.
   It must output `REJECT` to stdout and exit with code 1 if the log contains "evil" elements (such as disguised malicious shell commands, missing Rust ownership error context, or malformed CMake link errors).
   Ensure your Bash state machine correctly processes multi-line Rust borrow checker errors and CMake link failures.

2. **Fix the Build**:
   Our current build in `/app/project/` fails because CMake cannot find the correct path to the `libcore_ffi.so` shared library. 
   There is a legacy architecture diagram located at `/app/build_arch.png`. Use an OCR tool (like `tesseract`) to extract the text from this image. Somewhere in the diagram text, the correct absolute system path for the shared library is documented (e.g., `/usr/local/lib/secret_build_path/`).
   Write this exact path into a file at `/home/user/library_path.txt`.
   Then, patch the `CMakeLists.txt` in `/app/project/` to use this path so that the build completes successfully. Also fix the Rust code in `/app/project/src/lib.rs` which currently has a borrow checker error preventing the library from compiling.

Provide a fully working `/home/user/log_sanitizer.sh` and fix the build. Our automated test suite will run your sanitizer against a hidden corpus of clean and evil logs.