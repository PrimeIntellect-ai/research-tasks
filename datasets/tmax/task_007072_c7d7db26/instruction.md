You are a systems programmer working on the CI/CD pipeline for a custom Web Application Firewall (WAF) written in C. The project is located at `/home/user/waf-project`.

Currently, the CI pipeline (`/home/user/waf-project/ci_build.sh`) is failing during the linking phase. The project depends on a set of internal shared libraries, but their link order is constantly changing as developers add new dependencies. 

Instead of hardcoding the link order in the Makefile, the dependencies are now mapped out in `/home/user/waf-project/deps.txt` as a simple directed acyclic graph (adjacency list format).

Your task is to fix the CI pipeline using **only Bash** by completing the following steps:

1. **Dependency Resolution**: Write a bash script at `/home/user/waf-project/resolve_deps.sh` that reads `deps.txt`. It must perform a topological sort of the graph to determine the correct GCC link order. 
   - A library must appear *before* the libraries it depends on. 
   - The script must format the output as standard GCC link flags (e.g., `-lwaf -lparser -llog -lcrypto`).
   - The script must write this exact string to `/home/user/waf-project/flags.txt`.

2. **Patch Processing**: The security team has provided a patch file `/home/user/waf-project/security.patch`. Apply this patch to `waf_engine.c` to fix a vulnerability.

3. **CI/CD Pipeline Fix**: Create a patch file at `/home/user/waf-project/ci_fix.patch` that modifies `ci_build.sh` so that it:
   - Executes `./resolve_deps.sh` before `make`.
   - Reads the generated `flags.txt` and exports it as the `LDFLAGS` environment variable before invoking `make`.

4. **Execution**: Apply your `ci_fix.patch` to `ci_build.sh` and run `/home/user/waf-project/ci_build.sh`. If everything is correct, the C program will compile successfully, link correctly, and output a success log to `/home/user/waf-project/build_success.log`.

**Constraints**:
- Use only Bash, coreutils, and standard CLI tools (no Python, Perl, etc.).
- Do not modify the Makefile or C files directly; use patches and environment variables as specified.