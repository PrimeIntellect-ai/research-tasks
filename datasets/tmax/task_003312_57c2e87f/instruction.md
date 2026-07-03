You are tasked with fixing a broken staging deployment. We have an NGINX reverse proxy running locally as the current user, listening on port 8080. It currently returns a `502 Bad Gateway` error because the upstream Rust service is either not running or binding to the wrong address.

The source code for the upstream service is provided as a vendored package at `/app/upstream-service-1.2.0`. 

Your objectives are:
1. Identify the port NGINX is attempting to reverse-proxy to by inspecting its configuration file at `/home/user/nginx/nginx.conf`. You might want to use text processing tools like `grep` and `awk` to extract this dynamically.
2. Inspect the Rust service in `/app/upstream-service-1.2.0`. There is a bug in the code where it fails to bind to the correct port expected by NGINX. Fix the source code.
3. Build the Rust service for release.
4. We use a staged deployment directory structure. Create a new release directory at `/home/user/deploy/releases/v2/`.
5. Copy the compiled Rust binary into this new release directory.
6. Update the symlink at `/home/user/deploy/current` to point to your new `v2` release directory.
7. Start the Rust service from the `current` directory in the background.
8. Once you verify `curl http://localhost:8080` returns a successful response (HTTP 200), run the load test script `/home/user/test_load.py` and pipe its output to `/home/user/metrics.txt`.

Ensure the service remains running and the symlinks are correctly configured.