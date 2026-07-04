You are tasked with fixing a critical vulnerability in our internal backup pipeline. You need to write a Rust-based directory parser and archiver that securely handles symlinks, integrating with our existing backup microservices.

### Current Architecture & Services
Our system relies on two cooperating services (already running on your machine):
1. **Backup Storage Service (Flask)**: Runs on `http://127.0.0.1:5000`. It accepts `POST` requests to `/upload` with a multipart/form-data field named `file` containing a `.tar.gz` archive. 
2. **Metadata Store (Redis)**: Runs on `127.0.0.1:6379`. It tracks backup metrics.

### The Problem
Our naive backup scripts follow symlinks into infinite loops (causing disk exhaustion) or follow malicious symlinks pointing outside the backup target (e.g., pointing to `/etc/passwd`), leaking host files into the archives.

### Your Task
Create a Rust CLI application located at `/home/user/safe_archiver` (initialize it with `cargo new --bin safe_archiver`). 

The program must accept exactly two command-line arguments:
`safe_archiver <input_directory_path> <archive_name>`

**Validation Rules:**
Before archiving, your Rust application must recursively scan `<input_directory_path>`. It must **REJECT** the directory if it contains:
1. Any symlinks that form a circular loop (e.g., `A -> B` and `B -> A`).
2. Any symlinks that resolve to a path strictly outside of `<input_directory_path>`.

**Execution Flow:**
*   **If the directory violates any rule (Evil/Malicious):**
    The program must print an error to standard error, perform NO network operations, and immediately exit with status code `1`.
*   **If the directory is valid (Clean):**
    1. Create a compressed tarball (`.tar.gz`) of the directory's contents. Save it temporarily at `/tmp/<archive_name>`. (Preserve internal valid symlinks as symlinks in the tarball, do not resolve them into files).
    2. Read the `.tar.gz` and upload it via a `POST` request to `http://127.0.0.1:5000/upload` (using form field name `file`).
    3. Connect to the local Redis server (`127.0.0.1:6379`) and issue an `INCR backup:success` command.
    4. Exit with status code `0`.

**Constraints:**
* Use Rust. You may use external crates (like `tar`, `flate2`, `reqwest`, `redis`, `walkdir`) by adding them to your `Cargo.toml`.
* You must build the release version of your binary (`cargo build --release`) before you finish. The automated verifier will call `/home/user/safe_archiver/target/release/safe_archiver`.