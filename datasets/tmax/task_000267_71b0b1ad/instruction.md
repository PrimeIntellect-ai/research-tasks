You are tasked with forensic debugging and fixing a regression in a Bash-based web server called `bash-httpd`.

The source code is provided as a vendored Git repository at `/app/bash-httpd-repo`. The repository contains exactly 200 commits. At the initial commit (`HEAD~199`), the server correctly handled all standard requests. However, a regression was introduced somewhere in the commit history. 

When a client sends an HTTP request containing the header `X-Debug-Trace: true`, the server's connection handler experiences a convergence failure (an infinite loop) during header parsing, causing the request to hang indefinitely. 

Your tasks are:
1. Use `git bisect` (or any other debugging/tracing method) to identify the exact commit hash that introduced the convergence failure.
2. Write the full 40-character commit hash of the offending commit to `/app/buggy_commit.txt`.
3. Fix the bug in the `bash-httpd` code so that it successfully processes the `X-Debug-Trace: true` header without hanging, and properly breaks out of the header parsing loop to return an HTTP 200 OK response.
4. Start the fixed server listening on `127.0.0.1:8080`. The server must run in the background and remain active.

The server is launched via the script `./server.sh 8080` from within the repository directory.

Note: The automated verifier will send an HTTP GET request to `127.0.0.1:8080` with the `X-Debug-Trace: true` header and an `Authorization: Bearer secret-agent-123` header. It expects a timely HTTP 200 OK response with the body "OK". Make sure your fix handles these headers cleanly and allows the server to serve requests.