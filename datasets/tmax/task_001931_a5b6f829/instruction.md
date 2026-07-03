You are tasked with a critical forensics investigation and patch operation on a custom binary format parser written in Rust.

Recently, our production system started exhibiting strange behavior and crashing when processing certain user-uploaded files. We suspect a regression was introduced somewhere in the last 200 commits of our parser library, `lib_fmt_parse`. Additionally, we have observed suspicious system calls originating from the parser, suggesting some of these crashes might be driven by malicious payloads triggering an edge-case.

We have a zipped corpus of known "clean" and "evil" (malicious/crashing) files at `/app/corpus.zip`. However, the engineer who prepared this corpus locked it with a password and left the company. They left a sticky note on their desk with the password, which we have scanned and placed at `/app/clue.png`. 

Your objectives:
1. **Recover the Corpus**: Extract the password from `/app/clue.png` and decrypt `/app/corpus.zip`. You will find two directories inside: `clean/` and `evil/`.
2. **Diagnose the Regression**: A clone of the `lib_fmt_parse` repository is located at `/app/parser_repo`. The current `HEAD` is broken (fails on evil files, but might also exhibit unintended system behavior). The `main` branch has exactly 200 commits. The first commit (`HEAD~200`) is known to be good.
   - Use Git bisection to identify the exact commit that introduced the vulnerability. Be aware that some commits in the middle of the history contain broken builds (compile errors) that you will need to bypass or diagnose during your bisection.
   - Use `strace` or similar tools on the buggy parser against an `evil` file to understand the underlying mechanism of the exploit (e.g., what files is it trying to open? Is it looping indefinitely?).
3. **Build a Detector**: We cannot immediately roll back the repository. Instead, we need a standalone Rust-based validator to act as an edge-firewall. 
   - Create a Rust project at `/home/user/detector_project`.
   - Compile a binary to `/home/user/detector`.
   - Your binary must accept a single file path as a command-line argument.
   - It must parse the file just enough to detect the format edge-case without triggering it.
   - For any "clean" file, it must exit with status code `0`.
   - For any "evil" file, it must exit with a non-zero status code (e.g., `1`).

The automated verification suite will test your compiled `/home/user/detector` binary against the entire `clean/` and `evil/` corpus. 

Constraints:
- You must write the detector in Rust.
- Your final binary must be located exactly at `/home/user/detector`.
- Do not modify the test corpus files.
- The environment has standard tools installed, including `tesseract-ocr` for image reading, and a standard Rust toolchain.