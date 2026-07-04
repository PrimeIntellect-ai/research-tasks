You are a storage administrator managing a heavily fragmented disk. A legacy backup process has dumped files deep into a directory tree at `/home/user/storage_dump`. Disk space is critically low, and many files are misnamed, duplicated, or corrupted.

Your objective is to write and execute a Bash script `/home/user/dedup_archives.sh` that safely deduplicates and indexes these files without consuming additional disk space for the valid files.

Your script must perform the following actions:

1. **Discovery and Header Extraction**: Recursively navigate `/home/user/storage_dump`. For each file, determine its true MIME type by inspecting its binary headers (do not rely on file extensions, which are often wrong). Look specifically for `application/zip`, `application/gzip`, and `application/x-tar`.
2. **Archive Integrity Verification**: For files matching those three archive types, verify their integrity using the appropriate command-line tools (e.g., `unzip -t`, `gzip -t`, `tar -tf`). If an archive is corrupt or cannot be read, label its status as `Corrupt`. If it is a valid archive, label it `Valid`. Any other file type should be labeled `NotArchive`.
3. **Hard Link Deduplication**: For every `Valid` archive, compute its SHA256 checksum. Create a directory `/home/user/clean_archives/` and create a **hard link** to the valid archive inside it. The hard link must be named `<sha256>.<ext>` (where `<ext>` is `zip`, `gz`, or `tar` based on the true MIME type). If a hard link with that checksum already exists, do not create another one (this achieves deduplication).
4. **Symbolic Link Categorization**: Create a directory tree `/home/user/archive_index/<ext>/` (for `zip`, `gz`, and `tar`). Inside the corresponding directory, create a **symbolic link** named exactly as the original file's basename (e.g., `data.backup`), pointing to the hard link in `/home/user/clean_archives/`. 
5. **Atomic Report Generation**: Generate a report of all processed files. Because other system processes might read this report concurrently, you must write the report to a temporary file first and then atomically move it to `/home/user/inventory_report.csv`. 
   The CSV must have the following header: `Original_File_Name,Mime_Type,Status,SHA256`
   - `Original_File_Name`: Only the basename of the file.
   - `Mime_Type`: The extracted MIME type (e.g., `application/zip`, `text/plain`).
   - `Status`: `Valid`, `Corrupt`, or `NotArchive`.
   - `SHA256`: The SHA256 checksum of the file (or `N/A` if it's `NotArchive` or `Corrupt`).
   Sort the data rows alphabetically by `Original_File_Name`. Use tools like `awk` or `sed` to format the output.

Ensure your script handles files with spaces in their names. Execute your script to process the files.