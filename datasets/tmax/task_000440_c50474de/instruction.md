You are a mobile build engineer tasked with maintaining our build pipeline's local dependency cache service. 

We recently vendored a C-based graph resolution tool called `deptool` at `/app/vendored/deptool`. Unfortunately, the build is currently broken due to a deliberate perturbation in its `Makefile` (it has a typo in the compiler flag and requires a specific environment variable to compile). 

Your task:
1. Navigate to `/app/vendored/deptool` and fix the `Makefile`. You will need to figure out the typo and successfully compile the `deptool` binary.
2. Once compiled, the `deptool` binary takes a single argument (a file path) and outputs the dependent mobile build targets.
3. Create a purely Bash-based HTTP server script at `/app/server.sh` that listens on `127.0.0.1:8080`. You may use `nc` (netcat), `socat`, `awk`, or standard coreutils.
4. Your server must accept `POST /resolve` with a JSON payload like `{"file": "src/App.java"}`.
5. Extract the file name, pass it to `./deptool`, and return an HTTP 200 response with the `deptool` output as the body.
6. Implement a simple rate limiter in your bash server: allow a maximum of 2 requests per second. If a 3rd request comes in within the same second, return an HTTP 429 Too Many Requests response.
7. Run your server in the background so it is ready to receive requests.

Ensure your server correctly processes valid HTTP POST requests and strictly uses bash/coreutils (no Python/Node.js). You have full access to `/app/vendored/deptool` to analyze and fix the source.