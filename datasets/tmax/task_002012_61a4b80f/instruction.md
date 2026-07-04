You are tasked with debugging and fixing a failing build artifact server that is critical to our CI/CD pipeline. 

The server application is located at `/app/artifact_server.py`. It is a Python application that uses a vendored HTTP framework located at `/app/mini_http_framework`. 

Currently, the server is failing in two ways:
1. **Environment Misconfiguration:** The startup script `/app/start.sh` fails to launch the server. There is a misconfiguration regarding the `ARTIFACT_STORE_PATH` where the artifacts are supposed to be saved.
2. **Format Parsing Edge-Case Repair:** Once the server is running, developers have reported that uploading build logs with spaces in their filenames (e.g., `build log v2.txt`) causes the server to return a 500 Internal Server Error. The crash originates somewhere inside the vendored `mini_http_framework` package when it tries to parse multipart/form-data headers.

**Your objectives:**
1. Diagnose and fix the environment or script misconfiguration preventing the server from starting via `/app/start.sh`.
2. Debug the vendored `mini_http_framework` and fix the parsing logic so it correctly handles filenames with spaces in the `Content-Disposition` header.
3. Start the server by running `/app/start.sh` as a background process.

**Server Specifications:**
- The HTTP server must listen on `127.0.0.1:8080` for artifact uploads/downloads.
- The Admin TCP service must listen on `127.0.0.1:8081`.
- HTTP endpoints require the header `Authorization: Bearer dev-token-123`.
- The HTTP server expects multipart/form-data POST requests on `/upload` and GET requests on `/artifact/<filename>`.

Do not modify the business logic in `/app/artifact_server.py` unless strictly necessary; the core bug for the upload failure lies within the vendored `/app/mini_http_framework/parser.py`.

Once you have fixed the issues, execute the server using `/app/start.sh &` and ensure it stays running.