You are tasked with building a backup sanitization and processing pipeline in Rust for our internal backup infrastructure. As a backup administrator, you need to ensure that archived data is valid, not corrupted, and successfully logged into our tracking systems.

Our infrastructure consists of a multi-service environment:
1. **Redis**: Running on `localhost:6379`. Used to track processed backup IDs to avoid duplicate processing.
2. **Metadata API**: A Python Flask service running on `localhost:8080`. It exposes an endpoint `POST /register_backup` taking JSON `{"backup_id": "<id>", "file_count": <int>}`.

You need to write a Rust application at `/home/user/backup_processor` (create a new Cargo project here).
The application must support two subcommands:

### 1. `verify <directory_path>`
This command evaluates an extracted backup directory to determine if it is clean or corrupted ("evil").
- Recursively traverse the given directory.
- Look for nested archives (`.zip` or `.tar.gz`) and extract them temporarily to inspect their contents.
- Find the `backup.log` file in the root of the provided directory. This file contains multi-line records formatted as:
  ```
  BEGIN FILE: <relative_path>
  CHECKSUM: <sha256>
  END FILE
  ```
- **Validation Rules**:
  - Every file listed in `backup.log` MUST exist and its SHA256 checksum MUST match the file's actual content.
  - No executable files (`.sh`, `.elf`, or files with execute permissions) are allowed anywhere in the directory or inside nested archives.
  - If the directory is perfectly clean, the command MUST exit with code 0 and print `ACCEPT`.
  - If any validation fails, the command MUST exit with code 1 and print `REJECT`.

We have provided a corpus of test backups in `/app/corpus/clean` and `/app/corpus/evil`. Your `verify` logic must successfully `ACCEPT` all directories in the clean corpus and `REJECT` all directories in the evil corpus.

### 2. `daemon <spool_dir> <dest_dir>`
This command runs continuously.
- Watch the `<spool_dir>` for new `.tar.gz` backup files using file watching (e.g., `notify` crate).
- When a new archive appears, extract it to a temporary location.
- Run your `verify` logic on the extracted directory.
- If it passes validation:
  - Extract the `backup_id` from a file named `ID.txt` in the archive.
  - Check Redis (`SISMEMBER processed_backups <backup_id>`). If it exists, skip it.
  - If not in Redis, send a POST request to `http://localhost:8080/register_backup` with the backup ID and total file count.
  - Add the `backup_id` to Redis (`SADD processed_backups <backup_id>`).
  - Move the original `.tar.gz` file to `<dest_dir>`.
- If it fails validation, delete the `.tar.gz` from the spool directory.

**Integration test**: Start Redis and the Metadata API using the provided `/app/start_services.sh` script. Then run your daemon watching `/home/user/spool` and moving valid backups to `/home/user/processed`.

Please complete the Rust application and ensure both the verifier and daemon work correctly.