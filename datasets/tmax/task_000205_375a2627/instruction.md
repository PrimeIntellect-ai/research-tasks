You are tasked with rescuing a Web Application Firewall (WAF) migration project. We are replacing a legacy black-box payload scorer with a new Rust-based shared library, orchestrated by a Python scanner.

However, the developer left the project in a broken state:
1. The new Rust implementation in `/home/user/rust_waf/` fails to compile due to a module structure issue (a circular import/dependency error preventing the build).
2. The Rust library computes a hazard score for payloads, but it lacks the final classification threshold.
3. The legacy engine, a stripped binary located at `/app/legacy_scorer`, contains the ground-truth classification logic. 

Your objectives are:
1. **Fix and Build**: Troubleshoot and modify the Rust project in `/home/user/rust_waf/` so that `cargo build --release` successfully produces the shared library (`target/release/librust_waf.so`).
2. **Analyze**: Inspect or interact with the stripped binary `/app/legacy_scorer`. It takes a payload string as its first CLI argument, prints the hazard score, and exits with a specific status code if the payload is deemed "EVIL" versus "CLEAN". Reverse-engineer or probe this binary to determine the exact numerical threshold it uses to distinguish clean payloads from malicious ones.
3. **Implement**: Write a Python script `/home/user/detector.py`. This script must:
   - Accept a directory path as a command-line argument (e.g., `python3 /home/user/detector.py /app/corpus/clean`).
   - Iterate through all files in the given directory.
   - Read the contents of each file.
   - Use Python's `ctypes` to pass the file contents to the `compute_hazard` function exported by the compiled `librust_waf.so`. (The function signature is `uint32_t compute_hazard(const char* payload);`).
   - Compare the returned score against the threshold you discovered from the legacy binary.
   - Output a JSON dictionary to `/home/user/results.json` mapping the absolute file path to either `"CLEAN"` or `"EVIL"`. If the script is run multiple times, it should update or overwrite `results.json` with the latest directory's results.

To succeed, your `detector.py` script must perfectly classify an adversarial corpus of web requests. You can test your logic manually, but the automated verification will run your script against the hidden evaluation datasets.