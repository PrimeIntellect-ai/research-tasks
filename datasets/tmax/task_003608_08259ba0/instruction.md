I am a storage administrator managing a legacy data archiving cluster. Our old storage arrays dumped metadata snapshots into `/home/user/spool/` as compressed binary files with the `.enc` extension. We need a way to programmatically query this metadata to track disk space usage, but the system that originally generated them is dead.

We do have a recovered executable, `/app/storage_decode`, which decompresses these files. It is a stripped binary without documentation, but I've figured out that it reads compressed data from `stdin` and writes decompressed data to `stdout`. 

I need you to build a Go-based microservice that acts as an API for these files.

Here are your requirements:
1. Write a Go HTTP server that listens on `127.0.0.1:9090`.
2. Implement a single endpoint: `POST /api/v1/inspect`. The request body will be a JSON object like:
   `{"filepath": "/home/user/spool/snapshot_1.enc"}`
3. When a request is received, your Go service must:
   a. Read the specified file.
   b. Pass its contents through the `/app/storage_decode` binary via stdin to get the decompressed bytes on stdout.
   c. Parse the decompressed binary output. The format is strictly:
      - 4 bytes Magic Number: `0xDEADC0DE` (Big Endian)
      - 4 bytes Length `N`: Unsigned integer (Big Endian) representing the length of the trailing JSON payload.
      - `N` bytes: A UTF-8 JSON string containing the metadata snapshot.
   d. The embedded JSON string will look like this: `{"volume_id": "vol-99A", "used_bytes": 104857600, "free_bytes": 524288000, "inode_usage": 0.15}`.
   e. Calculate the disk space usage percentage as a float: `(used_bytes / (used_bytes + free_bytes)) * 100`.
   f. Return an HTTP 200 JSON response strictly formatted as: `{"volume": "vol-99A", "usage_percent": 16.66}` (round `usage_percent` to 2 decimal places).
4. **Audit Logging:** Every successful query must be logged to `/home/user/audit.csv`. You must ensure atomic writes/appends to this file so concurrent HTTP requests don't corrupt the log. The CSV format must be exactly: `<Unix_Timestamp_Seconds>,<volume_id>,<usage_percent>` (e.g., `1690000000,vol-99A,16.66`). Include a header row `timestamp,volume,usage_percent` if the file does not exist.

Please write, compile, and run the Go service so it is ready to accept requests.