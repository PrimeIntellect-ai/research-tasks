You are an infrastructure systems engineer tasked with fixing and hardening a locally vendored reverse proxy service. Our CI/CD pipeline recently broke because the proxy is returning 502 Bad Gateway errors. Additionally, a recent security audit revealed that the proxy lacks basic input sanitization, leaving us vulnerable to malicious payloads.

You need to fix the vendored package, implement a request filtering module in Go, and write a bash-based CI integration script to verify the behavior. 

**Part 1: Fix the Vendored Reverse Proxy**
We vendor our proxy source code at `/app/safe-router-1.1.0`. 
1. The build pipeline fails. Investigate and fix the `Makefile` in the package directory.
2. The proxy currently hardcodes its upstream Unix socket to `/var/run/broken.sock`, which causes a 502 Bad Gateway error. Modify `main.go` so that it instead reads the upstream socket path from the `UPSTREAM_SOCK` environment variable. 

**Part 2: Implement the Security Filter**
Inside `/app/safe-router-1.1.0`, there is a file named `filter.go` containing the function:
`func IsMalicious(req *http.Request) bool`
Currently, this returns `false` for all requests. You must implement logic to return `true` (reject) if a request meets ANY of the following criteria:
- The URL path contains directory traversal sequences (`../` or URL-encoded equivalents like `%2e%2e%2f`).
- The `X-Forwarded-Host` header is present and does not match the `Host` header.
- The `User-Agent` header contains the substring `sqlmap` or `nmap` (case-insensitive).

To test your implementation, we have provided two corpora of raw HTTP requests in `/app/corpus/evil/` and `/app/corpus/clean/`. 
The application has a built-in test command: `./safe-router verify --corpus /app/corpus` which will run your `IsMalicious` function against all files in those directories.

**Part 3: Build the CI/CD Integration Script**
Write a bash script at `/home/user/ci-run.sh` that automates the deployment and testing of this proxy. The script must:
1. Build the `safe-router` binary.
2. Create a directory structure for the socket at `/home/user/backend/`.
3. Create a symbolic link `/home/user/active-upstream.sock` pointing to `/home/user/backend/app.sock`.
4. Export the `UPSTREAM_SOCK` environment variable pointing to the symbolic link.
5. Run the proxy's internal corpus verification command (`./safe-router verify --corpus /app/corpus`).
6. Exit with a status code of `0` ONLY if the proxy builds successfully and the verification passes (100% of the evil corpus is rejected, 100% of the clean corpus is allowed).

Make sure `/home/user/ci-run.sh` is executable. You can test your workflow manually before finalizing the script.