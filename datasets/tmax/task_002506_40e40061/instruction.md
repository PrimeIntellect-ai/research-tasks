You are a deployment engineer tasked with rolling out an update for a backend service. 

We have a legacy interactive configuration generator that produces deployment credentials, and you need to automate its execution, write the new backend service in Rust, and create a robust deployment script.

Here are your instructions:

1. **Automate the Configuration Generator:**
   There is a pre-existing interactive script located at `/home/user/legacy_config_gen.sh`. When run, it prompts for three inputs sequentially:
   - `Enter deployment environment:` (You must answer `production`)
   - `Enter service name:` (You must answer `api_worker`)
   - `Confirm token generation (y/n):` (You must answer `y`)
   
   If answered correctly, the script generates a file at `/home/user/service_config.txt` containing a secret token (e.g., `TOKEN=<random_string>`).

2. **Implement the Rust Backend:**
   Write a Rust program at `/home/user/src/main.rs`. This program must:
   - Read the token from `/home/user/service_config.txt` (parsing the value after `TOKEN=`).
   - Start a standard HTTP server listening on `127.0.0.1:8443` using only Rust's standard library (`std::net::TcpListener` and `std::io`). No external crates (like `hyper` or `tokio`) are allowed.
   - For any incoming HTTP `GET /status` request, respond with a valid HTTP/1.1 200 OK response where the body is strictly the token value.
   - Keep running and accept multiple connections.

3. **Create the Deployment Script:**
   Write a bash script at `/home/user/deploy.sh` that automates the entire rollout process. The script must:
   - Be executable.
   - Use `expect` to run `/home/user/legacy_config_gen.sh` and feed it the required answers.
   - Compile the Rust backend using `rustc /home/user/src/main.rs -o /home/user/api_server`.
   - Start the `/home/user/api_server` in the background (daemonize it) so it continues running after the script exits.
   - Wait 2 seconds for the server to initialize.
   - Perform a health check by querying `http://127.0.0.1:8443/status`.
   - Write a log file at `/home/user/deploy_success.log` with the exact contents: `Rollout complete. Active token: <token_value_from_curl>`.

Ensure your deployment script handles errors robustly. Leave the Rust server running in the background when you are finished.