You are a forensics analyst investigating a compromised internal authentication system. The attacker modified the system's compiled authentication daemon to include a backdoor token generation algorithm, allowing them to bypass normal authentication flows.

Your task consists of two parts:

**Part 1: Restore the Compromised Service Architecture**
The system consists of three cooperating services located in `/app/`:
1. `redis-server` (Standard Redis caching server)
2. `api_gateway.py` (A Python Flask application handling HTTP requests)
3. `auth_daemon` (The compromised compiled C ELF binary that processes token requests)

The configuration file `/app/config.json` was corrupted by the attacker. You must edit this file and start the services so that the end-to-end authentication protocol works.
- Redis should listen on its default port (`127.0.0.1:6379`).
- `auth_daemon` must be started. It listens on a Unix domain socket at `/tmp/auth.sock` by default.
- `api_gateway.py` must be started. It runs on `127.0.0.1:5000`. 
- You must adjust `/app/config.json` so that `api_gateway.py` correctly points to the Redis instance and the `auth_daemon` Unix socket. 
- You can test the flow by sending a POST request to `http://127.0.0.1:5000/auth` with JSON `{"username": "testuser"}`.

**Part 2: Reverse Engineer the Backdoor Token Logic**
We need to scan our enterprise logs for attacker-generated backdoor tokens. To do this, we need a standalone script that perfectly replicates the compromised `auth_daemon`'s token generation algorithm.

1. Reverse engineer the `/app/auth_daemon` ELF binary (using tools like `objdump`, `strings`, `ltrace`, `strace`, or python's `pwntools`). 
2. Identify the algorithm used to generate the token when the daemon is queried.
3. Write a Python 3 script at `/home/user/backdoor_token.py`.
4. Your script must take exactly one command-line argument (the username) and print ONLY the resulting backdoor token string to standard output.

Example usage of your script:
`python3 /home/user/backdoor_token.py testuser`

Ensure your Python script is bit-exact equivalent to the daemon's generation logic for any alphanumeric string up to 64 characters.