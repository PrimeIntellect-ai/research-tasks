You are acting as an artifact manager for a binary repository. We have received an incoming consolidated payload from our build servers, but the artifacts are heavily nested. 

Your task is to write a Python script at `/home/user/process_artifacts.py` and run it to curate these binaries.

Here are the requirements:
1. There is a tarball located at `/home/user/incoming/payload.tar`.
2. Inside this tarball are multiple `.zip` files.
3. Inside those `.zip` files are various files, but we only care about the binary blobs ending in `.bin`.
4. Your Python script must extract all `.bin` files from the nested archives and place them directly into a single flat directory: `/home/user/curated_binaries/` (create this directory if it doesn't exist).
5. After extraction, the script must compute the SHA-256 checksum for each `.bin` file in the `/home/user/curated_binaries/` directory.
6. Finally, generate a manifest file at `/home/user/manifest.sha256`. The manifest must contain the SHA-256 checksums and the base filenames, formatted exactly like the standard `sha256sum` output (e.g., `[64-char-hash]  [filename.bin]`), with exactly two spaces between the hash and the filename.
7. The lines in `/home/user/manifest.sha256` must be sorted alphabetically by the filename.

Ensure your Python script handles the nested archive extraction and manifest generation programmatically. Run your script so the final state is achieved.