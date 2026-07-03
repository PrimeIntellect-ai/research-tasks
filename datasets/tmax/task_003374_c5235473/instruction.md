You are an application security engineer tasked with analyzing and securing a vulnerable multi-service web application. The application consists of three cooperating services located in `/app/`:
1. Nginx reverse proxy (`/app/nginx/`)
2. A Rust Actix-web backend handling authentication (`/app/backend/`)
3. A Redis instance for session state tracking (`/app/redis/`)

**Stage 1: Multi-Service Assembly**
The services are currently disconnected and misconfigured.
- Start the Redis server on its default port (`6379`).
- Fix the Nginx configuration at `/app/nginx/nginx.conf` so that requests to port `8080` are proxied to the Rust backend on port `8081`. 
- Ensure the Rust backend connects to the local Redis instance (adjust the `.env` file in `/app/backend/` to point `REDIS_URL` to `redis://127.0.0.1:6379`).
- Compile and start the Rust backend using `cargo run --release` in the background. Start Nginx with the corrected config.

**Stage 2: Vulnerability Analysis & Log Parsing**
The backend's login flow (`/api/login?redirect=<url>`) contains a critical Open Redirect vulnerability that can be escalated to SSRF because the server attempts to fetch metadata from the `redirect` URL before returning the 302 response. You must reverse engineer the compiled payload logs in `/app/logs/suspicious.log` to understand the pattern of attacks currently exploiting this.

**Stage 3: Developing the Rust WAF Filter**
Your primary objective is to write a standalone Rust command-line application that acts as a log parser and WAF filter. 
- Create a new Rust project at `/home/user/waf_filter`.
- The program must read URLs from standard input (one URL per line).
- For each URL, it must output exactly `CLEAN` or `EVIL` to standard output.
- It must accurately detect the Open Redirect / SSRF payloads (e.g., protocol smuggling, IP obfuscation, internal metadata IP `169.254.169.254`, localhost bypasses).

**Stage 4: Evaluation**
Your filter will be tested against two corpora provided in `/app/corpus/`:
- `/app/corpus/evil/`: Contains files with malicious redirect URLs.
- `/app/corpus/clean/`: Contains files with legitimate, benign redirect URLs.

To complete the task, your compiled Rust binary at `/home/user/waf_filter/target/release/waf_filter` must be able to process any concatenated list of these URLs via `stdin` and perfectly classify them without false positives or false negatives.