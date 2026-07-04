You are a backup administrator dealing with a legacy data transfer from an old localized server. You have received a compressed archive located at `/home/user/legacy_backups.tar.gz`.

This archive contains a set of `.zip` files, which in turn contain multiple log files with the `.log` extension. Because these logs originated from a legacy European system, their text is encoded in ISO-8859-1 (Latin-1), not UTF-8.

Your task is to write and execute a Rust program that automates the extraction, parsing, character conversion, and renaming of these legacy records.

Specifically, you must:
1. Extract `/home/user/legacy_backups.tar.gz` to access the nested `.zip` files.
2. Create a Rust Cargo project in `/home/user/archive_processor`.
3. The Rust program must:
   - Programmatically extract the contents of the `.zip` files.
   - Read each `.log` file, properly decoding it from ISO-8859-1 to UTF-8.
   - Parse the first line of each log file. The first line always strictly follows the format `ARCHIVE-ID: <id_string>` (e.g., `ARCHIVE-ID: 77A2X`).
   - Save the converted UTF-8 content (including the first line) to a new directory `/home/user/processed_logs/`.
   - The new filename must be exactly `<id_string>.txt` (where `<id_string>` is the parsed ID from the first line).
4. Run your Rust tool to process all the logs.
5. Create a final report file at `/home/user/processed_manifest.txt` that lists the base filenames of all the newly created files in `/home/user/processed_logs/`, sorted alphabetically (one filename per line, e.g., `1001.txt`).

Constraints:
- All resulting `.txt` files must be valid UTF-8.
- You may use any necessary standard Bash commands alongside your Rust program.
- You can add third-party crates (like `encoding_rs`, `zip`, etc.) to your Rust project as needed.
- Do not modify or delete the original `/home/user/legacy_backups.tar.gz`.