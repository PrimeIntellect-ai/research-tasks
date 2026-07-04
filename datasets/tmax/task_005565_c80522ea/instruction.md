You are a backup operator testing a staged deployment restore of our internal Rust-based email mailing list gateway. 

The filesystem backup has already been extracted to `/home/user/restore`. The deployment architecture consists of a local non-root Nginx reverse proxy serving requests to a Rust backend via a Unix domain socket.

When we attempt to start the restored deployment and hit the health endpoint, Nginx returns a 502 Bad Gateway. We suspect this is due to a misconfiguration in the upstream socket path between Nginx and the Rust application.

Your task is to fix the staged deployment and verify the restore:
1. Investigate the Nginx configuration located at `/home/user/nginx.conf` and the Rust application source located in `/home/user/restore/app`.
2. Identify and resolve the Unix domain socket path mismatch causing the 502 error. You may modify either the Nginx config or the Rust source code to make them match.
3. If you modify the Rust code, recompile it using `cargo build --release` inside `/home/user/restore/app`.
4. Start the Rust backend application in the background (`/home/user/restore/app/target/release/mailgate`).
5. Start the Nginx reverse proxy in the background using the provided config: `nginx -c /home/user/nginx.conf`.
6. Once both services are running, verify the restore by making an HTTP GET request to `http://127.0.0.1:8080/health`.
7. Save the exact HTTP response body from the health endpoint to a verification file located at `/home/user/restore_success.log`.

Ensure that the final output file `/home/user/restore_success.log` contains only the raw body of the successful response (e.g., no HTTP headers from curl, just the text returned by the Rust backend).