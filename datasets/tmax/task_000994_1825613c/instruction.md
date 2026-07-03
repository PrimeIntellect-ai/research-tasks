You are acting as an automated artifact manager curating a repository of binary files. 

You have been provided with a batch of uploaded developer artifacts in a single uncompressed tarball located at:
`/home/user/incoming/release_batch.tar`

This tarball contains a mix of nested archives (`.tar.gz`, `.tar.bz2`, and `.zip`). Some of these nested archives may be corrupted due to incomplete uploads.

Your objective is to write and execute Bash commands to perform the following curation pipeline:

1. **Extraction:** Extract `release_batch.tar` into a temporary working directory `/home/user/processing`.
2. **Integrity Verification:** Find all nested archives within `/home/user/processing`. Test each archive for integrity using standard tools (e.g., `gzip -t`, `bzip2 -t`, `unzip -t`). 
3. **Curation:** For every *valid* archive, extract its contents into `/home/user/extracted`. Discard/ignore the corrupted archives.
4. **Filtering and Path Manipulation:** Search through `/home/user/extracted` for all binary artifacts, specifically files ending with `.bin` or `.so`. 
5. **Flattening:** Copy all found `.bin` and `.so` files into a single flat directory at `/home/user/curated`. (Assume all target files have unique base names, so no overwriting will occur).
6. **Final Archiving:** Create a new compressed gzip tarball of the curated directory at `/home/user/curated_artifacts.tar.gz`. The tarball should contain the `curated` directory at its root.
7. **Manifest Generation:** Generate a SHA256 manifest of the curated files. Create a file at `/home/user/manifest.txt` where each line contains the SHA256 checksum and the base filename (e.g., `[hash]  filename.bin`), sorted alphabetically by filename. Use standard `sha256sum` output format but strip out the directory paths so only the basename appears.

Constraints:
- Use only standard bash built-ins, coreutils, and standard archive utilities (`tar`, `gzip`, `bzip2`, `unzip`).
- Do not write scripts outside of the terminal; execute the commands directly or write a shell script and run it.