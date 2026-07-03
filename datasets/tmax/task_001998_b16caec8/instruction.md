You are a technical writer managing a vast, deeply nested documentation repository. To avoid duplicated content, your team heavily relies on symlinks to cross-reference guides and API references. However, this has led to a critical issue: some authors have inadvertently created infinite symlink loops (e.g., `guide_A` links to `folder_B`, which links back to `guide_A`).

These loops are crashing our automated backup and documentation generation pipelines. 

You need to complete two main objectives using standard Bash tools:

**Objective 1: Fix the Vendored Doc Compiler**
We use a third-party documentation generation tool located at `/app/vendored/doc_compiler_v2.1`. Recently, a bug was introduced into the package that causes it to hang infinitely when it encounters a symlink loop during its build process. 
1. Diagnose and fix the shell script inside `/app/vendored/doc_compiler_v2.1` so that it safely parses directories without following infinite loops. 
2. The compiler must still be able to find and process all standard `.md` files without hanging.

**Objective 2: Build a Loop Detector**
Before we run the compiler on any new documentation branches, we need a sanitization filter.
1. Write a Bash script at `/home/user/validate_doc_tree.sh`.
2. The script must accept a single directory path as an argument (e.g., `./validate_doc_tree.sh /path/to/docs`).
3. The script must analyze the directory tree. If it detects **any** infinite symlink loops within that directory, it must exit with code `1` (reject).
4. If the directory is perfectly clean (no infinite symlink loops), it must exit with code `0` (accept).
5. The script must be robust enough to handle deep directory trees and complex loop topologies without hanging itself.

**Objective 3: Manifest Generation**
After fixing the compiler and writing the detector, you will find a log file at `/home/user/sync_requests.log` containing multi-line records of directories attempting to sync. 
1. Use your `validate_doc_tree.sh` to filter out the corrupted directories listed in the log.
2. For all *clean* directories, use `find` to locate all `.md` files inside them, generate their SHA256 checksums, and save the sorted list to `/home/user/safe_docs_manifest.txt` in standard `sha256sum` format.