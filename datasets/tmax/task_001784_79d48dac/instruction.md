You are helping a technical writer package a raw documentation repository for secure distribution. The writer has a disorganized directory of files and needs a robust tool to compute checksums and package them into an archive.

Your task is to write a Rust command-line application that processes a documentation directory, generates a manifest of file checksums using memory-mapped I/O, and creates a compressed archive.

**Specific Requirements:**
1. **Project Setup:** Create a new Rust binary project at `/home/user/doc_packager`.
2. **Directory Traversal:** The program must recursively traverse the directory located at `/home/user/docs_raw`.
3. **Memory-Mapped Hashing:** For every file found (excluding directories themselves), calculate its SHA-256 checksum. You **must** use memory-mapped I/O to read the file contents during the hashing process (e.g., using the `memmap2` crate).
4. **Manifest Generation:** Generate a JSON manifest file at `/home/user/docs_packaged/manifest.json`. The JSON should be a single object where the keys are the file paths *relative to the `docs_raw` directory* (using forward slashes `/`) and the values are the lowercase hex-encoded SHA-256 checksums.
   *Example:* `{"ch1/intro.md": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"}`
5. **Archive Creation:** Create a gzip-compressed tarball at `/home/user/docs_packaged/archive.tar.gz`. This archive must contain all the files from `docs_raw`. The file paths inside the archive must be relative to the root of `docs_raw` (i.e., extracting the tarball should not create a `docs_raw` parent directory, but just its contents).

**Notes:**
- You will need to create the output directory `/home/user/docs_packaged` if it doesn't exist.
- You can use external crates like `sha2`, `hex`, `memmap2`, `walkdir`, `tar`, `flate2`, and `serde_json` in your `Cargo.toml`.
- Run your Rust program to complete the packaging process. Ensure both the manifest and the archive are successfully generated in the target location before finishing.