You are tasked with recovering and organizing a series of system configuration changes from a batch of compressed Write-Ahead Log (WAL) files and ELF binaries. 

As part of our configuration management system, we use a custom Python package called `walparser` to extract state changes. However, the system is currently broken.

Here is what you need to do:

1. **Fix and Install the Vendored Package**:
   We have vendored the source code for `walparser-0.5.1` at `/app/walparser-0.5.1`. 
   Currently, trying to install it (e.g., `pip install .`) fails because of a deliberate disruption in its `setup.py` (it enforces a missing environment variable check that was meant for CI). Figure out the required environment variable or patch `setup.py`, then install the package in the local environment.

2. **Bulk Rename and Decompress**:
   In `/home/user/backups/`, there are hundreds of gzipped files named `backup_<id>.wal.gz`. 
   You need to bulk rename these files to `state_<timestamp>.wal.gz`. To find the timestamp, you must read the first 8 bytes of the *uncompressed* WAL stream (which represents a 64-bit integer Unix timestamp in little-endian format). Do this efficiently without extracting the entire files to disk.

3. **Parse and Extract Configurations**:
   Using the installed `walparser` package, process each renamed `state_<timestamp>.wal.gz` file. The package provides a `walparser.parse_stream(file_obj)` function that takes a file-like object (e.g., from Python's `gzip` module) and returns a list of configuration dictionaries.
   
4. **Generate a Manifest**:
   Create a manifest file at `/home/user/manifest.json`.
   It should be a JSON dictionary mapping the *new* filename (e.g., `state_1620000000.wal.gz`) to an object containing:
   - `checksum`: The SHA256 hash of the *compressed* `.gz` file.
   - `keys`: A sorted list of all unique configuration keys modified in that WAL file (extract the string from the `key` field of every dictionary returned by `walparser.parse_stream`).

Your solution will be evaluated by an automated script that calculates the F1 score of the extracted configuration keys and checksums against a golden reference. You must achieve a score of at least 0.95.