You are an AI assistant helping a technical writer organize and sanitize a massive trove of legacy documentation bundles before publishing them through a newly built, multi-service rendering pipeline.

You have two main objectives:
1. Fix the broken documentation rendering pipeline.
2. Write a Bash script to safely unpack, sanitize, and validate documentation bundles.

### Phase 1: Pipeline Configuration
There is a multi-service stack located in `/app/doc_stack/`. It consists of:
- **Nginx** (Reverse Proxy, meant to listen on port 8080)
- **Flask** (Markdown Rendering API, listening on port 5000)
- **Redis** (Caching layer, listening on port 6379)

Currently, the services fail to communicate. A startup script `/app/doc_stack/start.sh` launches them, but the configuration is incomplete. 
Your task:
- Modify `/app/doc_stack/nginx.conf` so that requests to `/api/render` are correctly proxied to the Flask application.
- Fix the Flask environment configuration `/app/doc_stack/.env` so it successfully connects to Redis (it is currently trying to reach a non-existent remote host).
- Ensure that you can successfully send markdown text via `curl -X POST http://127.0.0.1:8080/api/render --data-binary "# Hello"` and receive the rendered HTML output.

### Phase 2: Documentation Sanitizer Script
The documentation comes in "doc-bundles". A doc-bundle is a file that has been nested in a specific legacy format:
1. It is a `.tar` archive.
2. Inside the tar archive, there is a single file named `payload.gz`.
3. Inside `payload.gz` is a single `.zip` file.
4. Inside the `.zip` file are multiple `.md` (Markdown) files.

Some bundles are malicious and contain macros that could execute commands or inject bad scripts into our rendering pipeline. You must write a Bash script at `/home/user/process_archive.sh` that takes a single file path as an argument.

Requirements for `/home/user/process_archive.sh`:
- It must accept a doc-bundle path as its first argument (`$1`).
- It must dynamically decompress the nested archive structure (Tar -> Gz -> Zip) into a temporary directory.
- It must read all `.md` files extracted.
- **Validation (The Adversarial Filter):** If ANY of the `.md` files contain the exact strings `<script>`, `<iframe`, or `<!-- SYSTEM_EXEC:`, the script MUST immediately delete the temporary files and exit with return code `1` (rejecting the bundle).
- **Transformation:** If the bundle is clean, the script must use `sed` or `awk` to replace all occurrences of the word `[CONFIDENTIAL]` with `[REDACTED]` across all extracted `.md` files.
- **Output:** For clean bundles, the script must concatenate all transformed `.md` files, output the combined text to standard output (`stdout`), and exit with return code `0`.

To help you develop and test your script, there are test corpora located at `/home/user/corpora/clean/` (50 clean bundles) and `/home/user/corpora/evil/` (50 malicious bundles). Your script must flawlessly preserve the clean files and reject the evil ones. 

Your final deliverables must be the corrected configurations in `/app/doc_stack/` and the fully functioning `/home/user/process_archive.sh` script.