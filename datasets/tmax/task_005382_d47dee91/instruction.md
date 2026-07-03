You are a deployment engineer tasked with rolling out a high-performance Rust update for a critical log-filtering component in our monitoring stack. 

Currently, an Nginx reverse proxy receives logs on port 8080 and forwards them to a legacy Bash script (`/app/legacy_filter.sh`) managed by a systemd user service (`log-filter.service`). The filtered logs are then sent to a Redis backend, which is normally inaccessible directly, but can be reached via a pre-established SSH tunnel on port 6379.

Your task has two parts:

1. **Write the Rust Replacement:**
Analyze the behavior of the existing legacy oracle at `/app/legacy_filter.sh`. This script takes a single raw log string via standard input and prints a transformed, normalized string to standard output. 
Write a Rust program at `/home/user/new_filter.rs` and compile it to `/home/user/new_filter`. Your Rust program must be functionally identical (bit-exact output) to the legacy script for any given standard input.

2. **Reconfigure the Services:**
Update the user-level systemd service located at `/home/user/.config/systemd/user/log-filter.service` to use your new Rust executable (`/home/user/new_filter`) instead of the legacy script. 
Additionally, you need to establish a local port forward using SSH so that the Rust service can communicate with the Redis backend. Create a background SSH tunnel that forwards local port 9999 to `localhost:6379`. Use the existing SSH keys in `/home/user/.ssh/`.

Ensure your Rust program is successfully compiled, the systemd service is reloaded and restarted, and the SSH tunnel is active. Automated tests will verify the bit-exact output of your Rust binary against the oracle, as well as the end-to-end flow from Nginx through your filter to Redis.