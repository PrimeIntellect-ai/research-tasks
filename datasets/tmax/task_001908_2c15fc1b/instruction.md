You are an artifact manager responsible for curating incoming binary repositories for a secure supply chain. You need to build an automated Go-based validation filter that analyzes incoming archive files (`.zip` and `.tar.gz`) to ensure they meet strict security and structural policies.

Your tasks:

1. **Extract Policy Information:**
   There is a photographed label of the latest policy at `/app/policy_label.png`. Use standard OCR tools (like `tesseract`, which is installed) to read the text on this label. It contains a critical string in the format `APPROVED_PREFIX: <SomeString>`. Note this `<SomeString>` value.

2. **Develop the Go Artifact Filter:**
   Write a Go program at `/home/user/artifact_filter.go` and compile it to `/home/user/artifact_filter`. 
   
   The program must accept a single command-line argument: the absolute path to an archive file (`.zip` or `.tar.gz`).
   `./artifact_filter <path_to_archive>`

   The program must classify the archive as "clean" (exit code 0) or "evil" (exit code 1) based on the following rules:
   * **Integrity:** The archive must be valid and not corrupted.
   * **Path Traversal Prevention (Zip/Tar Slip):** No file or directory entry in the archive may resolve to a path outside the intended extraction root. Entries containing `../`, absolute paths (like `/etc/passwd`), or malicious symlinks that escape the root must cause the archive to be rejected.
   * **Policy Prefix:** Every single file and directory inside the archive MUST be contained within a top-level directory whose name exactly matches the `<SomeString>` extracted from the image. For example, if the prefix is `MY_PROJ`, an entry named `MY_PROJ/bin/app` is valid, but `OTHER_PROJ/bin/app` or a file at the root like `readme.txt` is invalid.

3. **Test Your Filter:**
   Ensure your compiled binary at `/home/user/artifact_filter` accurately exits with `0` for safe archives and `1` for malicious or non-compliant archives. 

Do not rely on external Go dependencies (like third-party archive libraries); use the standard library `archive/tar`, `archive/zip`, and `compress/gzip`.