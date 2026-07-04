You are an AI assistant acting as an automated artifact manager curating binary repositories. 

A background process is rapidly dumping Write-Ahead Log (WAL) files into a staging directory at `/home/user/staging`. Because of how the writer operates, it occasionally leaves incomplete records if it crashes or is actively writing. 

Your objective is to write and execute a Go program (`/home/user/curator.go`) that safely parses these WAL files, applies a configuration filter, and extracts the curated binary payloads to a repository directory (`/home/user/repo`) using atomic write patterns.

Here are the specific requirements:

1. **Configuration:**
   Read the configuration file at `/home/user/config.json`. It contains a JSON object like this:
   `{"min_level": <integer>, "allowed_prefix": "<string>"}`

2. **Parsing the WAL files:**
   Read all `.wal` files in `/home/user/staging/`.
   Each WAL file contains multiple log entries formatted exactly as follows:
   ```
   [START]
   LEVEL: <integer>
   PREFIX: <string>
   PAYLOAD: <base64 encoded string>
   [END]
   ```
   Because of potential race conditions with the writer, some entries might be missing the `[END]` tag. You must **ignore** any entry that does not have a matching `[END]` tag before the next `[START]` or the end of the file.

3. **Filtering & Extraction:**
   For each fully valid entry, check if its `LEVEL` is greater than or equal to `min_level` AND its `PREFIX` exactly matches `allowed_prefix`.
   If it passes, base64-decode the `PAYLOAD`.

4. **Atomic Writes:**
   Write the decoded binary payload to the repository directory `/home/user/repo/`.
   The filename must be `<PREFIX>_<MD5_of_decoded_payload>.bin`.
   To ensure another process doesn't read a partially written file, your Go program must use an **atomic write**: write the data to a temporary file (e.g., ending with `.tmp`) in the same directory first, and then rename it to the final `.bin` filename.

5. **Logging:**
   After processing all files, your Go program must create a file at `/home/user/summary.txt` containing a single integer representing the total number of perfectly valid, successfully extracted, and written `.bin` artifacts.

**Starting State:**
- The configuration file exists at `/home/user/config.json`.
- The staging directory exists at `/home/user/staging/` and contains several `.wal` files.
- The repository directory exists at `/home/user/repo/` (currently empty).

Write your Go code, compile/run it, and ensure all matching payloads are properly decoded and atomically written to the repo directory.