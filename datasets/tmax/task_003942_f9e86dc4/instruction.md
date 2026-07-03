You are a backup administrator tasked with building a robust archive sanitization pipeline. Users often submit nested backup archives that occasionally contain dangerous symlinks or broken hard links intended for directory traversal attacks, as well as nested archives that hide these malicious files.

Your task is to build a shell script that safely processes these archives, neutralizing any threats while preserving legitimate backup structures. 

**Part 1: Fix the Compression Utility**
We require the use of `pigz` (Parallel GZIP) for fast repackaging of the archives. The source code for `pigz` version 2.8 has been provided at `/app/vendored/pigz-2.8`.
However, the system administrator made a mistake when modifying the `Makefile`, and it currently fails to compile.
1. Identify and fix the perturbation in `/app/vendored/pigz-2.8/Makefile`.
2. Compile the package.
3. Make the resulting `pigz` binary available at `/home/user/bin/pigz` and ensure it is executable and in your `$PATH`.

**Part 2: The Backup Sanitizer**
Write a Bash script at `/home/user/sanitize_backup.sh` that takes exactly two arguments:
`./sanitize_backup.sh <input_archive.tar.gz> <output_archive.tar.gz>`

The script must perform the following operations:
1. **Safe Extraction**: Extract the input archive into a secure, temporary working directory.
2. **Nested Archive Handling**: Recursively find and extract any nested `.tar.gz` or `.tar` archives within the extracted structure. When a nested archive is found (e.g., `data/internal.tar.gz`), extract its contents into a directory of the same base name (e.g., `data/internal/`), and then delete the original nested archive file. This must be done recursively until no `.tar` or `.tar.gz` files remain.
3. **Link Management (Sanitization)**: 
   - Scan the entire extracted directory structure for symbolic links.
   - You must *preserve* any symlink that points safely to a file or directory *within* the root of the extracted archive.
   - You must *delete* any symlink that points to an absolute path (e.g., `/etc/passwd`) or uses relative traversal to point outside the extracted root directory (e.g., `../../../../../var/log`).
4. **Atomic Write & Repackaging**: 
   - Once sanitized, repackage the directory contents into a new `.tar.gz` file using the `tar` command combined with your compiled `pigz` utility.
   - To prevent incomplete writes from being read by downstream backup processors, you must implement an atomic write: package the output to `<output_archive.tar.gz>.tmp`, and only after the compression completely succeeds, move it to the final `<output_archive.tar.gz>`.

**Verification:**
An automated test suite will invoke your `/home/user/sanitize_backup.sh` script against two datasets: a clean corpus of normal backups, and an adversarial corpus of malicious backups (containing traversal links and deeply nested zip-bombs). Your script must preserve 100% of the safe files/links while successfully destroying 100% of the malicious links.