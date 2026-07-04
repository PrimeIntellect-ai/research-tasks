Our custom backend service is failing, causing our reverse proxy to return 502 Bad Gateway errors. The backend crashes because it occasionally receives malformed payload files that are not properly sanitized. Furthermore, our automated backup script is writing archives to the wrong directory because it's running in a restricted environment, and our logs are not being rotated. 

Please perform the following system administration and development tasks:

1. **Information Recovery (Vision):**
   The previous administrator left an architecture diagram at `/app/architecture.png`. Use OCR (e.g., `tesseract`) to extract the text from this image. Somewhere in the image text, there is a key-value pair specifying the absolute path for the main backup directory (e.g., `SECRET_BACKUP_LOCATION=/path/to/dir`). Identify this directory path.

2. **Fix the Backup Script (Idempotent Shell Scripting):**
   There is a backup script at `/home/user/scripts/backup.sh`. It is executed by a task runner with a minimal environment (meaning `PATH` is extremely restricted and environmental variables are stripped). 
   Modify `/home/user/scripts/backup.sh` so that it:
   - Sets a robust `PATH` internally so commands like `tar` and `gzip` work.
   - Idempotently creates the target backup directory (the one you extracted from the image) if it doesn't exist.
   - Tars and gzips the contents of `/home/user/backend/data/` and saves it to the target backup directory as `data_backup.tar.gz`.
   - Your script must use bash built-ins, coreutils, and standard CLI tools only.

3. **Log Configuration & Rotation:**
   Create an idempotent bash script at `/home/user/scripts/rotate_logs.sh` that rotates the backend log file located at `/home/user/backend/logs/server.log`. 
   - If the log file is larger than 1MB (or if you run the script manually for testing), it should rename the file to `server.log.1` (overwriting any existing `server.log.1`), compress it using `gzip`, and truncate the original `server.log` to zero bytes without disrupting the file descriptor. 

4. **Write the Payload Sanitizer (C Programming):**
   The backend service crashes because it reads unsanitized text payloads. You must write a standalone C program at `/home/user/backend/sanitizer.c` and compile it to `/home/user/backend/sanitizer`.
   This program must act as a filter. It will take a file path as a command-line argument.
   - It should read the file.
   - It must reject (exit with code 1) any file that contains the exact substring `DROP_TABLE` or contains any non-printable ASCII characters (excluding standard whitespace like `\n`, `\r`, `\t`).
   - It must accept (exit with code 0) files that do not violate these rules.
   - We have provided two test corpora: 
     - `/app/corpus/evil/`: Contains malformed/malicious payloads.
     - `/app/corpus/clean/`: Contains valid payloads.
   - Your compiled `sanitizer` must exit with `1` for ALL files in the evil corpus, and exit with `0` for ALL files in the clean corpus.

Ensure all scripts are executable and the C program is successfully compiled. Our automated verification suite will run your scripts and test your C program against the hidden corpora.