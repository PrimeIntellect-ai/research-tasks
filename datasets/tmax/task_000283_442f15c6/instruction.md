You are a release manager preparing a new expression evaluation microservice for deployment. Before deploying, you must build and configure a Web Application Firewall (WAF) filter that protects the backend from ReDoS and resource exhaustion attacks caused by deeply nested mathematical payloads.

Your task consists of the following steps:

1. **Extract Security Policy**: You have been provided a voice memo from the CISO at `/app/audio/security_policy.wav`. Transcribe or listen to this audio file to find the maximum allowed parentheses nesting depth for expressions.

2. **Fix and Build the Rust Engine**: The core numerical algorithm engine at `/app/src/rust_engine/` has a Rust ownership/borrow checker bug preventing it from compiling.
   - Fix the bug in `src/lib.rs`.
   - Build it as a static library (`librust_engine.a`).

3. **Develop the Go WAF Filter**:
   - Initialize a Go module at `/app/src/waf_filter/`.
   - Write a Go program `main.go` that takes a file path as its first command-line argument.
   - The Go program must read the target file's contents (a mathematical expression string) and parse it to enforce the security policy:
     - **Rule A:** The expression must ONLY contain digits (`0-9`), operators (`+`, `-`, `*`, `/`), parentheses (`(`, `)`), and spaces. Any other characters are forbidden.
     - **Rule B:** The parentheses nesting depth must NOT exceed the maximum limit you extracted from the audio file.
   - If the expression violates ANY rule, the program must print `EVIL` to standard output and exit with status code `1`.
   - If the expression is safe, the program must use `cgo` to link against the Rust static library you built, call its `evaluate_safe()` C-FFI function, print `CLEAN` to standard output, and exit with status code `0`.

4. **Deploy**: Build your Go program and place the final executable exactly at `/app/bin/waf_filter`.

An automated CI system will test your binary at `/app/bin/waf_filter` against a corpus of clean and malicious payloads. You must ensure it reliably accepts all clean payloads and rejects all evil payloads.