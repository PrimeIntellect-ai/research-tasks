You are tasked with setting up an automated uptime monitoring pipeline for an SRE environment. This involves fixing a broken monitoring client, building a URL sanitization filter to prevent SSRF (Server-Side Request Forgery) attacks, generating TLS certificates interactively, and configuring a secure logging pipeline.

**Phase 1: Fix the Vendored Prober**
We use a custom Go-based HTTP prober CLI located at `/app/vendored/prober-cli`. However, the tool currently fails to build and execution times out instantly due to perturbations in its source code. 
1. Fix the `Makefile` so it correctly builds the binary from the existing source files.
2. Fix the hardcoded timeout bug in the Go code so that requests default to a 5-second timeout instead of failing immediately.
3. Successfully compile the binary to `/home/user/prober-cli`.

**Phase 2: Build the SSRF URL Sanitizer**
You must write a Go program at `/home/user/sanitizer.go` and compile it to `/home/user/sanitizer`. 
The program must read a list of URLs from standard input (one per line) and print only the safe URLs to standard output.
You must DROP (filter out) any URL that points to:
- Loopback addresses (e.g., 127.0.0.0/8, ::1)
- Link-local addresses or AWS Metadata endpoint (169.254.169.254)
- Private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
- Any URL with a scheme other than `http` or `https`
Valid, public URLs must be preserved exactly as they appeared.

**Phase 3: TLS and Test Endpoint Setup**
1. We have a certificate generation script at `/app/scripts/gen_cert.sh`. It interactively prompts for a passphrase: `Enter passphrase:`.
2. Write an `expect` script at `/home/user/auto_cert.exp` to automate executing this script and passing the passphrase `sre-secure`. This will generate `/home/user/server.crt` and `/home/user/server.key`.
3. Start a basic HTTPS web server (in Go or bash/socat) listening on `127.0.0.1:8443` serving the `/health` endpoint with a `200 OK` response using the generated certificates. Run this in the background.

**Phase 4: Pipeline Execution and Logging**
1. Create a group named `sre-logs` (if it doesn't exist).
2. Create a bash script `/home/user/monitor.sh` that processes a dummy list of URLs (you can create `/home/user/test_urls.txt` containing `https://127.0.0.1:8443/health` and `https://google.com` to test).
3. The script must pipe the URL list through your `/home/user/sanitizer`, and for every safe URL, execute the `/home/user/prober-cli`.
4. Append the results to `/var/log/prober.log`. 
5. Ensure `/var/log/prober.log` is owned by `user:sre-logs` and its permissions are strictly set to `640` (read/write for owner, read for group, none for others).

Ensure all services are running and the log file exists with the correct permissions when you finish.