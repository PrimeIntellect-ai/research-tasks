We have a Go-based HTTP key-value store in `/home/user/repo` with its own custom Write-Ahead Log (WAL) implementation for crash recovery. Recently, our automated tests started reporting intermittent startup crashes related to corrupted WAL replays, and statistical analysis points to a regression introduced somewhere in the last 200 commits on the `main` branch. 

Your tasks are as follows:
1. Use `git bisect` and system call tracing (`strace`) or simple reproduction scripts to identify which commit introduced the regression. The bug causes the server to panic intermittently when encountering a specific sequence of partial WAL writes.
2. Fix the bug on the `main` branch (do not just revert the commit; fix the underlying incomplete read handling logic in `wal.go`).
3. We have an image at `/app/auth_token.png` containing our development environment's admin authorization token. Extract this token from the image (e.g., using `tesseract`).
4. Build and start the fixed Go server. It must listen on `127.0.0.1:9000`.
5. You must pass the extracted token to the server via the `ADMIN_TOKEN` environment variable so it can authenticate incoming requests. Run the server in the background so it remains active.

Do not change the server's API structure. The server must be running and listening by the end of your interaction.