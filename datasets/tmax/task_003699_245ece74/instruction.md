You are helping a technical writer migrate and secure a legacy documentation system. The previous system relied on incremental tar backups, but it was recently discovered that some of the backups contain path traversal (Zip Slip) payloads maliciously injected by a compromised dependency. 

You need to write a script or set of scripts (you may use Python, Bash, Perl, or any combination) to perform the following pipeline:

1. **Archive Integrity Verification & Incremental Backups**: 
   Look in `/home/user/docs_backup/`. You will find a series of incremental tar archives named `backup_0.tar`, `backup_1.tar`, `backup_2.tar`, etc.
   Before extracting, verify the integrity of each archive. If any file path inside a `.tar` archive contains `../` or an absolute path starting with `/`, you must NOT extract that archive. Instead, move the malicious archive to `/home/user/quarantine/`.
   Extract the safe archives in sequential order into `/home/user/extracted_docs/` to properly reconstruct the final state of the incremental backups.

2. **Multi-line Log Record Parsing**:
   The old system left a log file at `/home/user/migration.log`. The log has a multi-line format where each entry looks like this:
   ```
   [ERROR]
   DocID: 1045
   Reason: Corrupted metadata
   File: some_doc.md
   ---
   ```
   Parse this file and delete any file in `/home/user/extracted_docs/` that is listed under `File:` in an `[ERROR]` block.

3. **Recursive Directory Traversal & Bulk File Renaming**:
   Traverse `/home/user/extracted_docs/` recursively. Bulk rename any file with the extension `.HTM` to `.html` (making it lowercase). Leave other files unchanged.

4. **Integration with Stripped Binary**:
   There is a proprietary, stripped indexing tool located at `/app/doc_indexer`. It is a black box. You must figure out how to run it to generate an index of the `/home/user/extracted_docs/` directory. (Hint: run it and analyze its output or reverse-engineer its arguments). It will output a binary file named `index.dat`. Place this file in `/home/user/extracted_docs/index.dat`.

5. **Serve the Documentation**:
   Write and start an HTTP server listening on `0.0.0.0:8080`. The server must implement:
   - `GET /api/index`: Returns the exact bytes of `index.dat`.
   - `GET /api/docs?file=<filename>`: Traverses `/home/user/extracted_docs/` and its subdirectories to find the file with the exact name `<filename>`. Returns its contents. If multiple files have the same name, return the first one found. If not found, return HTTP 404.

Keep the server running in the background or foreground so that our automated verification system can issue HTTP requests to test your work.