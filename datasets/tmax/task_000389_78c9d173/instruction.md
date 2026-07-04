I am an observability engineer setting up a new "Dashboards as Code" deployment pipeline. Developers keep committing poorly configured dashboards that either overload our production databases or crash the observability UI. I need you to build a secure, automated pipeline using a local Git repository, scheduled tasks, and a local validation hook.

Here is your environment:
- The dashboard metrics backend API has been started by a background service. It listens on `127.0.0.1:9090`.
- We have a set of test dashboard JSON files available in `/app/test_corpus/clean/` and `/app/test_corpus/evil/`.

Please complete the following setup:

1. **Port Forwarding:**
   The deployment tooling expects the backend API to be available on `127.0.0.1:8080`, but the service actually listens on `9090`. Configure a background process (using a tool like `socat`) that forwards TCP connections from `127.0.0.1:8080` to `127.0.0.1:9090`. Leave this running.

2. **Git Repository & Pipeline Setup:**
   - Create a bare Git repository at `/home/user/dashboards.git`.
   - Write a deployment script at `/home/user/deploy.sh`. This script must:
     - Clone or pull `/home/user/dashboards.git` into `/home/user/deploy_workspace`.
     - Find all `.json` files in the repository.
     - `POST` each JSON file's contents to `http://127.0.0.1:8080/api/dashboard` using `curl` (with header `Content-Type: application/json`).
   - Make the script executable.
   - Schedule `/home/user/deploy.sh` to run every minute using the current user's crontab.

3. **Validation Git Hook (The core task):**
   Developers will push their dashboard JSON files to `/home/user/dashboards.git`. To prevent bad configurations from ever being committed, create a `pre-receive` hook in the bare repository (`/home/user/dashboards.git/hooks/pre-receive`). 
   
   The `pre-receive` hook must be written in **Bash** and analyze the incoming blobs (using `jq` and `git cat-file`) for every updated or added `.json` file in the push.
   
   It must **reject** the push (exit non-zero) if ANY of the following rules are violated in ANY modified/added JSON file:
   - **Rule 1 (Rate Limit):** If the JSON contains a top-level key `"refresh_rate"`, its value MUST NOT be `"1s"`, `"5s"`, or `"10s"`.
   - **Rule 2 (Datasource Safety):** If the JSON contains a top-level key `"datasource"` with the value `"production"`, it MUST also have a top-level key `"mode"` set to EXACTLY `"read-only"`.

   If all files pass, the hook must exit 0 and allow the push. The hook must gracefully handle new branches (where the old revision is `0000000000000000000000000000000000000000`).

Ensure your hook correctly reads `oldrev newrev refname` from stdin, inspects only the changed/new files (ignoring deletions), and evaluates the strict JSON criteria above.