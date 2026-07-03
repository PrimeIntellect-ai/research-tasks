You are a storage administrator managing a pool of database write-ahead log (WAL) files. Space is running low, and you need to identify which WAL files can be safely archived or deleted. 

You have a directory located at `/home/user/wals` containing several large `.wal` files. There is also a simulated application workload script at `/home/user/trigger_db.py`. 

Your objectives are:
1. **File Watching:** Run the workload script in the background (`python3 /home/user/trigger_db.py &`). This script continuously writes to exactly *one* of the WAL files in the `/home/user/wals` directory. You must write a Python script that monitors the directory to identify which `.wal` file is currently active (being modified).
2. **Memory-Mapped Domain Parsing:** The inactive WAL files are quite large, so standard I/O might be slow. Using Python's `mmap` module, parse the binary structures of all *inactive* `.wal` files to find specific database transactions. 
    *   **WAL Format Refresher:** 
        *   A SQLite WAL file starts with a 32-byte header. Bytes 8-11 contain the database page size as a big-endian 32-bit integer.
        *   Following the header are frames. Each frame consists of a 24-byte frame header followed by the page data (which is exactly `page_size` bytes long).
        *   The first 4 bytes of the 24-byte frame header contain the database Page Number being written to (as a big-endian 32-bit integer).
3. **Identification:** You need to find all *inactive* `.wal` files that contain at least one frame writing to database Page Number `999`. These specific files contain obsolete transient data and are your "purge candidates".

Once you have identified the active file and the purge candidates, create a JSON report at `/home/user/report.json` with the following exact structure:
```json
{
  "active_wal": "db_X.wal",
  "purge_candidates": [
    "db_Y.wal",
    "db_Z.wal"
  ]
}
```
*Note: The `purge_candidates` array should only contain the base filenames, sorted alphabetically.*

Ensure your solution relies on memory-mapping (`mmap`) for the binary parsing, as this is a requirement for our storage auditing tools.