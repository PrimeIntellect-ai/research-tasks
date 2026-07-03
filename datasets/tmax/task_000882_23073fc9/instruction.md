You are acting as a storage administrator managing disk space and security for a log aggregation server. 

A set of compressed log archives has been uploaded to `/home/user/incoming_logs/`. However, we have been warned that some of these archives are malicious and attempt a "zip slip" attack—they contain file paths that try to break out of the extraction directory (e.g., using absolute paths starting with `/` or relative paths starting with `../` or containing `/../`).

To safely manage disk space and extract important metrics, you need to write and execute a Bash script that processes these archives **without extracting them to disk**.

Your script must perform the following tasks entirely in Bash using standard CLI tools:

1. **Scan for Malicious Archives**: Inspect the file list of every `.tar.gz` archive in `/home/user/incoming_logs/`. If an archive contains any file path that starts with `/`, starts with `../`, or contains `/../`, classify it as MALICIOUS.
2. **Process Safe Archives (Stream Processing & Data Parsing)**: For archives that are safe, read the log files inside them on the fly (streaming the contents without saving uncompressed files to disk). 
   - The logs contain multi-line error records formatted strictly like this:
     ```
     [YYYY-MM-DD HH:MM:SS] ERROR_START
     <variable number of message lines>
     Disk-Impact: <integer_bytes>
     [YYYY-MM-DD HH:MM:SS] ERROR_END
     ```
   - Parse these multi-line blocks and sum up the total `Disk-Impact` values across all safe archives.
3. **Generate a Manifest**: Generate a final report at `/home/user/processed_manifest.txt` with the following exact format:

```
SAFE_ARCHIVES:
<sha256sum> <filename>
<sha256sum> <filename>

MALICIOUS_ARCHIVES:
<filename>
<filename>

TOTAL_DISK_IMPACT: <total_integer_sum>
```
*Notes on the manifest format:*
- Under `SAFE_ARCHIVES:`, list the SHA-256 checksum of the compressed `.tar.gz` file, followed by a space, followed by just the basename of the file (e.g., `archive1.tar.gz`). Sort these lines alphabetically by filename.
- Under `MALICIOUS_ARCHIVES:`, list just the basename of the malicious archives. Sort these lines alphabetically by filename.
- `TOTAL_DISK_IMPACT:` should be the sum of all `Disk-Impact` integers found inside the log blocks of the safe archives.

Write the script, execute it, and ensure `/home/user/processed_manifest.txt` is created exactly as specified.