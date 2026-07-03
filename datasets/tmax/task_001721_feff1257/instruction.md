You are tasked with building a configuration tracking API for a legacy deployment system. 

We have a directory containing various deployment configuration files located at `/home/user/deployments`. We also have an audit log file located at `/home/user/audit/changes.log` which tracks configuration drift over time. Finally, there is a proprietary, stripped binary at `/app/hash_checker` that calculates custom integrity hashes of configuration files.

Your objective is to build a Python-based HTTP server that exposes the latest state and hashes of specific managed configurations.

Here are the specific requirements:

1. **Metadata-based File Search**: First, identify all `.ini` files within `/home/user/deployments` (and its subdirectories) that are group-writable (e.g., have the `g+w` permission). Ignore any files that do not have this permission.

2. **Multi-line Log Parsing**: The log file `/home/user/audit/changes.log` is potentially very large. Use memory-mapped I/O or efficient streaming in Python to parse it. The log consists of multi-line records formatted exactly like this:
```
---BEGIN RECORD---
File: <absolute_path_to_file>
Timestamp: <ISO-8601 timestamp>
Changes:
<variable number of diff lines>
---END RECORD---
```
For each of the group-writable `.ini` files you found, determine the *most recent* `Timestamp` associated with it in the log. 

3. **Binary Oracle Analysis**: The system provides a stripped binary `/app/hash_checker`. By experimenting with it, figure out how to pass one of the `.ini` file paths to it to generate a configuration hash. The binary prints a hex string to standard output. 

4. **Service Exposure**: Create and start a Python HTTP server listening on `127.0.0.1:9090`. The server must implement the following endpoint:
- `GET /status?file=<absolute_file_path>`
If the file is a group-writable `.ini` file found in step 1, the server must respond with an HTTP 200 status code and a JSON response in the following format:
`{"latest_update": "<timestamp from log>", "hash": "<output of /app/hash_checker>"}`

If the file is not found, is not group-writable, or has no log entries, return HTTP 404.

Leave your HTTP server running in the background or foreground so that our automated test suite can verify your implementation by sending HTTP requests to it. Ensure the server strictly adheres to the requested port (9090) and JSON schema.