I need your help organizing a messy project directory that contains recursive symlinks. We need to build a manifest of all the unique files, but standard tools like `find` are getting stuck in infinite loops.

Please write a Rust program that generates a checksum manifest of a directory while safely handling infinite symlink loops.

Here are the requirements:
1. Create a new Rust project named `manifest_builder` in `/home/user/manifest_builder`.
2. The program must take a directory path as a command-line argument (e.g., `cargo run -- /home/user/project_data`).
3. It must recursively traverse the provided directory. 
4. It must follow symlinks, but it **must not get stuck in infinite loops** (e.g., if a symlink points to its own parent directory).
5. For every *unique* regular file it finds (resolving all symlinks to their canonical, absolute paths to avoid duplicates), it must compute the SHA-256 checksum of the file's contents. Process both text and binary files.
6. The program must write the results to a file at `/home/user/manifest.txt`.
7. The format of `/home/user/manifest.txt` must be exactly:
   `<SHA256_HEX>  <CANONICAL_ABSOLUTE_PATH>`
   (Note: use exactly two spaces between the checksum and the path).
8. The lines in `/home/user/manifest.txt` must be sorted alphabetically by the canonical absolute path.

Once you have written and compiled the Rust program, run it against the directory `/home/user/project_data` so that `/home/user/manifest.txt` is populated correctly.