You are a backup administrator responsible for modernizing a legacy data archiving system. The system relies on three microservices that have been deployed but are currently misconfigured. Once the infrastructure is working, you need to write a highly robust shell script to pack data files into a custom streaming archive format.

### Part 1: Infrastructure Integration
The system consists of three services:
1. **Nginx** (supposed to run on port 80): Acts as the main gateway.
2. **Redis** (supposed to run on port 6379): Stores file metadata.
3. **Python Backup API** (supposed to run on port 5000): An internal service.

Currently, the services are not communicating correctly:
- Nginx's configuration at `/etc/nginx/sites-available/default` is missing the `proxy_pass` directive for the `/api/` location block, which should point to `http://127.0.0.1:5000/`.
- Nginx's `/data/` location block is currently pointing to the wrong root. It must serve files directly from `/app/backup_data/`.
- Redis is currently configured in `/etc/redis/redis.conf` to bind only to a Unix socket instead of `127.0.0.1`.
Fix these configurations and restart the necessary services using their standard init or systemctl commands (or direct binary invocation if systemd is unavailable, e.g., `nginx -s reload`).

### Part 2: The Archive Processor
Write a Bash script at `/home/user/archive_processor.sh`. This script will be used as a pipeline filter to process incoming backup jobs.

**Input:**
The script will receive a stream of newline-separated filenames on standard input (`stdin`). 

**Processing For Each Filename:**
1. **Metadata Retrieval & Encoding Conversion:** Connect to local Redis and fetch the value for the key `file_meta:<filename>`. This metadata is stored in raw `UTF-16LE` encoding. You must convert this to `UTF-8`.
2. **Data Retrieval:** Fetch the file's raw content via HTTP GET from Nginx at `http://127.0.0.1/data/<filename>`.
3. **Concurrent Logging:** To maintain an audit trail while multiple archivers run concurrently, you must safely append the string `[ARCHIVED] <filename>` (followed by a newline) to the file `/tmp/backup_audit.log`. You **must** use `flock` on a lockfile at `/tmp/audit.lock` to ensure your append operation is strictly atomic and thread-safe.
4. **Archive Stream Output:** For each file, print the following strictly formatted block to standard output (`stdout`):
```
---BEGIN_RECORD---
FILE: <filename>
META: <utf-8_converted_metadata>
PAYLOAD:
<raw_file_content_from_nginx>
---END_RECORD---
```

**Constraints:**
- Use only standard bash built-ins, coreutils, `redis-cli`, `curl`, `iconv`, and `flock`.
- Pay strict attention to standard stream redirection: all error messages must go to `stderr`, and only the exact archive format must go to `stdout`.
- Ensure no extra newlines are added to the payload section.