You are a storage administrator managing an automated data ingestion pipeline. We are running low on disk space because users are uploading malicious or malformed archives (zip bombs, directory traversal attacks, etc.) to our ingestion API. 

Our ingestion stack consists of three services running locally:
1. A Redis instance (port 6379) storing ingestion metadata.
2. A MinIO object storage instance (port 9000) for storing file chunks.
3. A Flask ingestion gateway (port 5000) that receives archive uploads.

Currently, the Flask gateway blindly accepts `.zip` and `.tar.gz` files and processes them. You need to write a Python validation and processing script `/home/user/pipeline/archive_filter.py` that acts as a secure middleware. 

Your script must implement a CLI that takes a path to an archive file:
`python3 /home/user/pipeline/archive_filter.py process <path_to_archive>`

The script must:
1. Safely inspect the archive (zip or tar.gz).
2. Reject the archive (exit with code 1 and print "REJECTED") if it contains:
   - Absolute paths or directory traversal attempts (e.g., `../` or `/etc/passwd`).
   - Symlinks or hardlinks pointing outside the archive.
   - Extremely high compression ratios indicative of a zip/tar bomb (e.g., uncompressed size > 50x compressed size, or uncompressed size > 100MB for a tiny archive).
3. Accept the archive (exit with code 0 and print "ACCEPTED") if it is completely safe.
4. For accepted archives, your script must split the safely extracted files into 1MB chunks, generate a JSON manifest (containing original file paths, chunk names, and SHA256 checksums), and upload the chunks to the `ingest-bucket` in MinIO, while saving the manifest JSON string to Redis under the key `manifest:<archive_filename>`.

We have provided a test harness in `/home/user/tests/run_tests.sh` that will evaluate your script against a hidden dataset of both safe and malicious archives. Ensure your script handles all edge cases. You will need to start the services using the provided `docker-compose.yml` in `/home/user/services/` before testing.