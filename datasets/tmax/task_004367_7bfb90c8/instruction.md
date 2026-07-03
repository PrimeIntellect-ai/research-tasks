You are a forensic analyst responding to a security breach. A threat actor exploited an open redirect vulnerability in our Rust-based authentication portal (`auth-svc`) to steal user session tokens. 

Your objective is twofold: 
1. Reconstruct the compromised environment to verify the authentication flow.
2. Write a Rust tool to analyze the attacker's evasion payloads and determine the destination of the stolen tokens.

### Part 1: Reconstruct the Environment (Multi-Service Flow)
The incident response team has provided the binaries for the involved services in `/app/services/`:
- `auth-svc`: The vulnerable Rust authentication backend. Listens on `127.0.0.1:8081`.
- `token-logger`: A dummy service simulating the attacker's drop server. Listens on `127.0.0.1:9090`.

You must configure and run a reverse proxy using `nginx` (running entirely in user-space) that binds to `127.0.0.1:8080`. 
Create your nginx configuration at `/home/user/nginx.conf`. It must:
- Run Nginx in the foreground (`daemon off;`).
- Store its PID in `/home/user/nginx.pid`.
- Store error logs in `/home/user/error.log` and access logs in `/home/user/access.log`.
- Route all requests starting with `/login` to `http://127.0.0.1:8081`.
- Route all requests starting with `/steal` to `http://127.0.0.1:9090`.

Ensure the services are started and functioning. A successful authentication flow `GET /login?user=admin&pass=admin&next=/steal` on the proxy (port 8080) should result in a redirect to the logger.

### Part 2: Evidence Analyzer Tool
The attacker used complex URL-encoding and protocol-relative payloads in the `next` parameter to bypass basic filters. 
You must write a Rust program that replicates the vulnerable routing logic to extract the exact domain the attacker redirected to.

Create a Rust project in `/home/user/payload_analyzer`. The compiled binary must be at `/home/user/payload_analyzer/target/release/analyzer`.

The program must take a single command-line argument (the raw `next` payload string) and output a single line to `stdout` based on the following strict rules:
1. URL-decode the input string completely (handle standard `%XX` encoding).
2. Strip any leading or trailing whitespace characters.
3. Determine the destination host:
   - If the string starts with `http://` or `https://`, parse the hostname.
   - If the string starts with `//` (protocol-relative), parse the hostname.
   - If the string starts with any other character (e.g., `/dashboard`), it is an internal redirect.
4. Output format:
   - If it is an internal redirect, print: `SAFE: <decoded_path>`
   - If it is an external redirect to `localhost`, `127.0.0.1`, or `corp.local`, print: `SAFE: <hostname>`
   - If it is an external redirect to any other host, print: `EXPLOIT: <hostname>`
   - If the URL is malformed or no hostname can be parsed from an external redirect, print: `INVALID`

Example:
`./analyzer "https://evil.com/drop"` -> `EXPLOIT: evil.com`
`./analyzer "%2F%2Fattacker.net%2Fpath"` -> `EXPLOIT: attacker.net`
`./analyzer "%2Fdashboard"` -> `SAFE: /dashboard`

Build your Rust application in release mode. Do not leave the Nginx process running in a way that blocks your terminal; background it appropriately after configuration.