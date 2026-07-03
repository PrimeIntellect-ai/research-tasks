You are a backup administrator for a legacy system. We are migrating old archival data, but our security team has flagged that the old backup manifests may contain "Zip Slip" payloads—maliciously crafted file paths intended to overwrite system files outside the target extraction directory (e.g., `../../../etc/passwd`).

Your task is to write a Rust command-line utility that sanitizes these backup manifests and outputs safe, renamed paths according to our company policy.

**Requirements:**

1. **Policy Extraction:**
   There is a scanned memo located at `/app/policy_memo.png`. You must use OCR (e.g., `tesseract`) to read this image. It contains a specific departmental prefix code and the exact quarantine path for malicious files. You must use this exact prefix and quarantine path in your Rust program.

2. **Rust Program Specification:**
   Write a Rust program. The compiled binary must be located at `/home/user/sanitizer/target/release/sanitizer` (create the cargo project in `/home/user/sanitizer`).
   
   The program must read from `STDIN`. The input will be a multi-line backup manifest log. Each record in the log is formatted as follows, separated by a line with exactly three dashes `---`:
   ```
   File: <filepath>
   Size: <bytes>
   Date: <YYYY-MM-DD>
   ---
   ```

   For each record, your program must:
   * **Parse the log:** Extract the `<filepath>`.
   * **Sanitize (Zip Slip Prevention):** The target extraction root is theoretically `/archive/`. 
     * If the `<filepath>` resolves to a location *inside* `/archive/` (e.g., `docs/../docs/file.txt` -> `/archive/docs/file.txt`), it is valid.
     * If the `<filepath>` attempts to escape the root (e.g., `../etc/shadow` or `docs/../../bin/bash`), you must re-root the base filename (e.g., `shadow` or `bash`) into the quarantine directory specified in the policy memo.
   * **Bulk Renaming Application:** Apply the departmental prefix from the policy memo to the *basename* of every file (both valid and quarantined).
   * **Output:** Print the final, sanitized absolute paths to `STDOUT`, one path per line. Do not print any other text.

3. **Constraints:**
   * Your program must handle complex path resolutions (e.g., collapsing `./` and `../`).
   * Do not create the files on disk; this tool is a string/path processor for the validation pipeline.

Ensure your compiled release binary is at `/home/user/sanitizer/target/release/sanitizer`. An automated fuzzer will test your binary against thousands of randomly generated multi-line logs to ensure it matches the strict security standard bit-for-bit.