It is 3 AM and you've been paged. The internal metrics aggregator system is failing. 

The system consists of three components currently running on the server:
1. Nginx (listening on port 8080)
2. A Go API service (listening on port 8081)
3. Redis (listening on port 6379)

These are started via `/app/start.sh` (already running). 

There are two distinct issues you need to resolve:

**Issue 1: Routing Configuration**
The Go service leaks goroutines when clients disconnect abruptly, which we've mitigated in the Go code, but the load balancer configuration is broken. Nginx is failing to route requests correctly to the Go API.
You must fix `/app/nginx.conf` so that any request to `http://localhost:8080/api/v1/<endpoint>` is correctly stripped of the `/api/v1` prefix and proxied to the Go service on `http://127.0.0.1:8081/<endpoint>`. 
For example, a request to `http://localhost:8080/api/v1/ping` should be proxied to `http://127.0.0.1:8081/ping`. 
Modify `/app/nginx.conf` and apply the changes so the routing works. Nginx is running as a daemon.

**Issue 2: Payload Recovery (Encoding Troubleshooting)**
During the outage, the Go service dumped corrupted serialized payloads into a crash directory. We have a compiled binary oracle `/app/oracle_decoder` that correctly recovers and decodes these specific corrupted hex-encoded payloads back to plain text. 
We need the decoding logic implemented in a script so we can integrate it into our Python-based forensics pipeline.
You must write a standalone script (in Python, Bash, or any language of your choice) at `/home/user/decoder`. It must accept exactly one command-line argument (a hex-encoded string), decode it exactly the same way `/app/oracle_decoder` does, and print the resulting decoded string to standard output.
You do not have the source code for `/app/oracle_decoder`, but you can execute it to analyze its inputs and outputs to deduce the encoding scheme. The encoding involves a combination of byte-level operations (such as XOR and reversing) but no complex compression.

Requirements:
- Fix the Nginx configuration so the end-to-end routing works.
- Create an executable file at `/home/user/decoder` that is functionally identical (bit-exact output) to `/app/oracle_decoder` for any valid hex-encoded string.
- Ensure your decoder handles edge cases (like empty strings) identically to the oracle.