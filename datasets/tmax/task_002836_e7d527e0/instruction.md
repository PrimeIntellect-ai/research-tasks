You are tasked with organizing and securing a custom project-file management system. This system allows developers to upload unified diffs (patches) and minimal assembly snippets via a REST API to update system components. 

However, the system currently lacks proper validation and routing, making it vulnerable to malicious patches (e.g., directory traversal) and dangerous assembly payloads (e.g., shellcode containing forbidden syscalls). 

Your goal is to build a C++ security filter and integrate it into a multi-service architecture.

**Step 1: The C++ Sanitizer & Router**
Create a C++ program at `/home/user/sanitizer` (compile from `/home/user/sanitizer.cpp`).
This program will act as a CLI-based validator and routing decision engine. It must accept a single file path as an argument:
`./sanitizer <path_to_payload_file>`

The payload files are standard text files containing either a Unified Diff or raw x86_64 Assembly.
Your C++ program must analyze the file contents and:
1. Return an exit code of `0` (Clean/Accept) if the file is safe.
2. Return an exit code of `1` (Evil/Reject) if the file is malicious.

**Rejection Criteria (Evil):**
- **Diffs:** Reject any patch that attempts to modify files outside the current working directory (e.g., contains `../` or absolute paths like `/etc/` in the `---` or `+++` headers).
- **Assembly:** Reject any snippet that contains syscalls commonly used for execution or privilege escalation (specifically, look for `execve`, `syscall` combined with `mov eax, 59`, or `int 0x80`).

**Step 2: Multi-Service Composition**
The system ships with a pre-installed application architecture in `/app/`. 
There are three services:
1. **Nginx Reverse Proxy:** Runs on port `8080`. Its configuration is at `/app/nginx/nginx.conf`.
2. **Storage Backend:** A dummy service running on port `9001` that accepts safe patches.
3. **Execution Backend:** A dummy service running on port `9002` that accepts safe assembly.

You must modify `/app/nginx/nginx.conf` so that:
- Requests to `/api/patch` are routed to the Storage Backend (port 9001).
- Requests to `/api/asm` are routed to the Execution Backend (port 9002).

**Step 3: Verification**
Once your C++ program is compiled at `/home/user/sanitizer` and Nginx is properly configured, start the services using the provided bash script: `/app/start_services.sh`.

We will automatically test your `/home/user/sanitizer` binary against a hidden corpus of clean and evil files. You do not need to start the web server for the corpus test, but Nginx must be running with the correct routing for the integration test.