You are tasked with creating a Rust-based automated file organizer and archiver to manage a messy stream of incoming project data. 

As a developer, I need a reliable background service that watches an incoming directory, parses and chunks large data files, archives them, and maintains a structured directory using symlinks and hard links for quick access.

Please write a Rust project in `/home/user/data_organizer` that does the following:

1. **File Watching:** Use the `notify` crate to watch the directory `/home/user/incoming/` for new files. 
2. **Data Parsing & Splitting:** When a new text file is dropped into `incoming/` (e.g., `raw_data.txt`), read it and split it into smaller files of exactly 50 lines each. Name the chunks `chunk_0.txt`, `chunk_1.txt`, etc.
3. **Link Management:** 
   - Create hard links of all generated chunks into `/home/user/debug_chunks/`.
   - Create a symbolic link at `/home/user/latest_data.txt` pointing to the original dropped file in `incoming/`.
4. **Archive Creation:** Compress all the newly created chunks into a single gzip-compressed tar archive located at `/home/user/processed/archive.tar.gz`. Use the `tar` and `flate2` crates.
5. **Completion:** Once the archive is created and all links are established, write the word "SUCCESS" to `/home/user/status.log` and have the Rust program exit cleanly.

**Setup Instructions for You:**
- You must create the necessary directories: `/home/user/incoming`, `/home/user/processed`, and `/home/user/debug_chunks`.
- Initialize a Rust binary project at `/home/user/data_organizer`.
- Add necessary dependencies to `Cargo.toml`.
- Write the Rust code in `src/main.rs`.
- Write a bash script at `/home/user/run_and_test.sh` that does the following:
  1. Compiles the Rust project (`cargo build --release`).
  2. Runs the compiled executable in the background.
  3. Waits for 2 seconds to ensure the watcher is active.
  4. Generates a test file named `/home/user/incoming/raw_data.txt` containing exactly 125 lines of text (you can write a simple loop to generate "Line 1", "Line 2", etc.).
  5. Waits for `/home/user/status.log` to be created.

To complete this task, write the code, build it, and run your `run_and_test.sh` script to verify it works. The final evaluation will inspect the contents of the `processed/` directory, the validity of the symlink and hard links, and the chunk sizes in the tar archive.