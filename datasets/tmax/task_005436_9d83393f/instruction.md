You are a container specialist managing a local microservice stack. We have an unauthenticated internal API that is suddenly receiving malformed, potentially malicious traffic from an exposed external ingress. Since you do not have root access to configure iptables, you need to implement a user-space application firewall (WAF) filter in C, integrate it into a local CI/CD testing pipeline, and deploy it via a user-space port forwarder to protect the backend services.

Your task is divided into three parts:

**Part 1: The C-based WAF Filter**
Write a C program located at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`. 
The program must:
1. Read a complete HTTP request payload (or raw text) from `stdin` until EOF.
2. Analyze the content for basic malicious patterns. Specifically, it must reject any input that contains the exact case-insensitive substrings:
   - `UNION SELECT`
   - `OR 1=1`
   - `<script>`
   - `DROP TABLE`
3. If ANY of these malicious patterns are found, the program must print "REJECTED" to `stdout` and terminate with exit code `1`.
4. If NONE of these patterns are found, the program must print "ACCEPTED" to `stdout` and terminate with exit code `0`.

**Part 2: The CI/CD Testing Pipeline**
Write a bash script at `/home/user/pipeline.sh` that tests your compiled `sanitizer`.
1. The script should iterate over all files in `/app/corpus/clean/`. It must pipe each file into `./sanitizer`. If the exit code is not `0`, the script should exit immediately with code `1`.
2. The script should iterate over all files in `/app/corpus/evil/`. It must pipe each file into `./sanitizer`. If the exit code is not `1`, the script should exit immediately with code `1`.
3. If all tests pass, the script prints "PIPELINE SUCCESS" and exits with code `0`.
*Note: Make sure your script has execute permissions.*

**Part 3: Multi-Service Composition & Port Forwarding**
We have two backend services already available on the system:
- **Backend API**: A Python service listening on `127.0.0.1:8081` (processes actual requests).
- **Audit Logger**: A Python service listening on `127.0.0.1:8082` (receives logs of rejected requests).

First, start the background services by running the provided script: `/app/start_services.sh`.

Then, write a robust bash script at `/home/user/proxy.sh` that acts as your user-space port forwarder. The script must:
1. Listen for incoming TCP connections on `127.0.0.1:8080` (e.g., using `socat` or `nc` in a loop).
2. For each incoming connection, read the payload and pass it through your `/home/user/sanitizer` binary.
3. If the sanitizer exits with `0`, forward the exact original payload to the Backend API (`127.0.0.1:8081`) and return its response to the client.
4. If the sanitizer exits with `1`, forward the exact original payload to the Audit Logger (`127.0.0.1:8082`), and return the string `HTTP/1.1 403 Forbidden\r\n\r\n` to the client.

Ensure `/home/user/proxy.sh` is running in the background before you finish the task. 

**Deliverables:**
- `/home/user/sanitizer.c` and the compiled `/home/user/sanitizer`
- `/home/user/pipeline.sh` (executable, passing all tests)
- `/home/user/proxy.sh` (executable, running, and actively routing traffic on port 8080)