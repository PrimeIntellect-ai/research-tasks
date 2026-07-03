You are a storage administrator managing a custom backup system. Recently, a critical vulnerability was disclosed: our backup restoration tool (`/app/restorer`) is vulnerable to "Zip Slip"-style attacks. Maliciously crafted backups can contain absolute paths (e.g., `/etc/shadow`) or directory traversals (e.g., `../../root/.ssh/authorized_keys`), causing the restorer to overwrite system files outside the target extraction directory.

We use a proprietary "Incremental Backup" (IBK) format. The `/app/restorer` tool is a stripped binary that extracts these files. 

Your task is to write a Python detection tool at `/home/user/detect_slip.py` that analyzes an IBK backup archive and determines if it is safe to extract or if it contains malicious path traversals.

### The IBK File Format
The IBK backup file is a **Gzip-compressed** stream. Once decompressed, it consists of a sequence of file records. Each record has the following binary layout:
1.  **Magic Header**: 4 bytes, always `IBK1` (ASCII).
2.  **Path Length**: 2 bytes, unsigned short (little-endian).
3.  **File Path**: UTF-8 string of length specified above.
4.  **Data Length**: 4 bytes, unsigned int (little-endian).
5.  **File Data**: Raw bytes of the file content, of length specified above.
6.  **Incremental Flag**: 1 byte. `0x00` means full backup, `0x01` means differential block.

The file contains back-to-back records until the end of the stream.

### Requirements for `/home/user/detect_slip.py`
*   It must accept a single command-line argument: the path to the backup file. Example: `python3 /home/user/detect_slip.py /path/to/backup.ibk.gz`
*   It must parse the headers of the compressed stream *without* necessarily loading the entire uncompressed data into memory (use `seek` or skipping techniques over the `Data Length` payload to be efficient).
*   It must inspect every `File Path` in the archive.
*   **Classification Rule**:
    *   If **any** file path in the archive starts with `/` (absolute path) or contains `../` or `..\` or ends with `..` as a path component (directory traversal), the script must print `MALICIOUS` to standard output and exit with status code `1`.
    *   If **all** file paths are safe (e.g., `var/www/html/index.php`, `config.json`), the script must print `SAFE` to standard output and exit with status code `0`.

To help you develop and test your tool, we have provided an adversarial corpus of backups:
*   `/app/corpus/clean/`: Contains safe backups.
*   `/app/corpus/evil/`: Contains malicious backups attempting directory traversal.

You can also interact with the provided `/app/restorer` binary if you need to observe the extraction behavior.