You are acting as a backup administrator for a legacy system. We are migrating our backup scripts to Rust. 

The system uses a proprietary archive format (used by our legacy tools). We have lost the source code for the legacy archiver, but we have a stripped compiled binary of the extractor located at `/app/legacy_unpacker` and the packer at `/app/legacy_packer`.

Your task is to write a secure archiving tool in Rust that packages a given directory into this proprietary format. You must reverse-engineer the archive format by interacting with `/app/legacy_packer` and `/app/legacy_unpacker`.

Additionally, the new archiver must act as a security filter against malicious file structures (e.g., a process racing to create malicious symlinks during backup). It must perform recursive directory traversal and handle symlinks carefully.

Security Requirements:
1. If the input directory contains ANY symlink that points outside the backup root (absolute or relative like `../../`), or contains circular symlinks, the archiver MUST reject the backup, print `MALICIOUS DIRECTORY DETECTED`, and exit with code 1.
2. If the directory is safe, it must produce the correctly formatted archive and exit with code 0.
3. You must use memory-mapped I/O (e.g., using the `memmap2` crate) for reading file contents to compute checksums efficiently.

Project setup:
- Initialize your Rust project at `/home/user/safe_archiver`.
- Your final compiled binary should be at `/home/user/safe_archiver/target/release/safe_archiver`.
- The CLI invocation must be: `./safe_archiver <input_directory> <output_archive_path>`

To validate your tool, there are two test corpora provided on the system:
- `/home/user/corpus/clean/`: Contains 5 subdirectories with safe files and safe intra-directory symlinks. Your tool must successfully archive 100% of these.
- `/home/user/corpus/evil/`: Contains 5 subdirectories with malicious symlinks (e.g., pointing to `/etc/passwd` or outside their root). Your tool must reject 100% of these with exit code 1.

Do not use external crates other than `memmap2`, `sha2`, and standard Rust libraries.