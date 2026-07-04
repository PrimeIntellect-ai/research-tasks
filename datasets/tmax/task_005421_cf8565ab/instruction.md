I need you to build a secure, automated project file organizer in Rust that integrates with our internal microservices.

Our system receives project archives from developers and automatically organizes them. However, we recently discovered that some archives contain "tar slip" (path traversal) vulnerabilities that overwrite system files outside the target extraction directory.

We have a multi-service environment located in `/app/`:
1. **Upload Service**: Runs on `127.0.0.1:5000`. It places uploaded `.tar` files into `/home/user/incoming/`.
2. **Analytics Service**: Runs on `127.0.0.1:5001`. It receives processing results and calculates an evaluation metric.

Your task is to write a Rust program (create it in `/home/user/organizer/`) that acts as the processing worker. It must do the following:
1. Continuously monitor `/home/user/incoming/` for new `.tar` files.
2. For each `.tar` file, safely extract it to `/home/user/projects/<archive_name_without_extension>/`.
3. **Security Requirement**: Prevent tar slip! Any file inside the archive whose extraction path would resolve outside the target project directory must be completely ignored (do not extract it).
4. **Organization Requirement**: For the safely extracted files, you must organize them by moving them into subdirectories within the project directory based on their file type:
   - ELF binaries (identified by the `\x7fELF` magic number, not just extensions) -> move to `bin/`
   - Text files (valid UTF-8 contents) -> move to `src/`
   - SQLite Write-Ahead Log (WAL) files (identified by the `SQLite format 3` or WAL header, or simply files named `*.wal`/`*.db`) -> move to `db/`
5. **Reporting**: After processing an archive, send a JSON POST request to `http://127.0.0.1:5001/report` with the following structure:
   ```json
   {
     "archive": "name_of_archive.tar",
     "extracted_bin": 2,
     "extracted_src": 5,
     "extracted_db": 1,
     "ignored_malicious": 3
   }
   ```
   (The integers represent the count of files placed in each category and the number of path-traversal files ignored).

To finish the task:
- Start the background services provided in `/app/start_services.sh`.
- Compile and run your Rust worker.
- Trigger the test sequence by running `/app/trigger_uploads.sh`, which will upload a batch of test archives.
- The Analytics service will grade your extraction and categorization accuracy. You must achieve a perfect parsing score (1.0).

Please leave your Rust program running in the background when you are done.