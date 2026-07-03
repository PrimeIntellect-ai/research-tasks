You are a script developer working on utilities for a CI/CD pipeline. Your team needs a tool to safely transport code patches through a strict reverse proxy that enforces rigid request validation and strips special characters. To bypass this temporarily, we need to hex-encode the modified lines of unified diffs.

Write a Rust utility at `/home/user/obfuscate_patch.rs` that reads a unified diff patch from `stdin` and writes the obfuscated patch to `stdout`.

Rules for the Rust utility:
1. Process the input line by line.
2. If a line starts with `+` (but is not `+++`), keep the `+` character, but replace the rest of the line (excluding the newline character) with its lowercase Hexadecimal encoded equivalent.
3. If a line starts with `-` (but is not `---`), keep the `-` character, but replace the rest of the line (excluding the newline character) with its lowercase Hexadecimal encoded equivalent.
4. All other lines (including `+++`, `---`, `@@` headers, and unmodified context lines) must be printed exactly as they are.

Next, simulate a CI/CD step by creating a bash script at `/home/user/build_and_test.sh` that does the following:
1. Compiles your Rust script using `rustc` into an executable named `/home/user/obfuscate_patch`.
2. Reads the file `/home/user/test.patch` and pipes it into your compiled executable.
3. Redirects the standard output of the executable to `/home/user/artifact.patch`.
4. Exits with a status code of 0.

Ensure your bash script is executable (`chmod +x`). Once you have written both files, execute `/home/user/build_and_test.sh` to generate the final artifact.