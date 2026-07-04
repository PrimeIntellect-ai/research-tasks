You are tasked with securing a configuration management system that tracks changes via incremental and differential backups. The system consists of multiple cooperating services:
- **MinIO** (S3-compatible storage) running on port 9000.
- **Redis** running on port 6379 (stores metadata).
- **Config Tracker Service** (a Go web service) running on port 8080.

The tracker service receives differential backup chunks of config files via HTTP POST requests to `/upload`. These chunks are encoded in a custom binary format to support legacy systems:
- **Magic Bytes**: `BKP1` (4 bytes)
- **Encoding String Length**: uint8 (1 byte)
- **Encoding**: ASCII string (length specified by the previous byte, e.g., "UTF-16LE", "Windows-1252", "UTF-8")
- **Payload Size**: uint32 (4 bytes, little-endian)
- **Payload**: The actual configuration diff text, encoded in the specified character encoding.

Recently, attackers have been injecting malicious commands into these backups using non-standard character encodings to bypass basic text filters. 

Your task consists of two parts:

1. **Write an Admission Controller (Classifier/Filter)**
Create a Go CLI tool at `/home/user/filter.go` and compile it to `/home/user/filter`. The tool must accept a single file path as a command-line argument:
`/home/user/filter <filepath>`
It must parse the binary format, extract the payload, and convert it from the specified encoding to UTF-8. 
If the decoded payload contains the exact substrings `EXEC_BASH` or `/dev/tcp/`, it must exit with status code `1` (rejected).
If the payload is clean, it must exit with status code `0` (accepted).
To help you test, there is a corpus of files in `/app/corpus/clean/` (which should all be accepted) and `/app/corpus/evil/` (which should all be rejected).

2. **Integrate the Filter into the Services**
The Go Tracker Service source code is located at `/home/user/app/server.go`. Currently, it accepts all uploads and saves them to MinIO and Redis.
Modify `/home/user/app/server.go` so that when a file is uploaded, it saves the file to a temporary location, executes your `/home/user/filter` against it, and:
- If the filter exits with `0`, proceeds to save the file to MinIO and Redis as usual, returning HTTP 200.
- If the filter exits with `1`, deletes the temporary file, skips storage, and returns HTTP 403 Forbidden.

You can start the services by running `/app/start.sh`. Ensure your Go environment is configured correctly and any necessary dependencies (like `golang.org/x/text`) are installed.