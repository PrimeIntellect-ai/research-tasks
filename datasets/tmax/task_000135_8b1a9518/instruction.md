You are a compliance analyst responsible for securing a binary ingestion pipeline. The system runs locally and uses Nginx, a lightweight backend service, and Redis to log audit trails. 

Your task consists of three main parts:
1. **Service Configuration (CSP & Proxying)**
   The Nginx configuration at `/app/nginx/nginx.conf` is incomplete. You must modify it so that:
   - It enforces a strict Content Security Policy by adding the header: `Content-Security-Policy: default-src 'none'; frame-ancestors 'none';` to all responses.
   - It proxies requests for the `/upload` endpoint to the backend service listening on `http://127.0.0.1:9090`.

2. **Binary Analysis & Validation in C**
   You must write a C program at `/home/user/elf_validator.c` and compile it to `/home/user/elf_validator`. The backend service relies on this executable to check if uploaded binaries are compliant.
   The program must take a single command-line argument (the file path to analyze).
   It must return exit code `0` if the file is compliant ("clean") and exit code `1` if it is non-compliant ("evil").
   
   A file is considered **non-compliant (evil)** if ANY of the following conditions are met:
   - It is not a valid 64-bit ELF file (e.g., missing magic bytes, or not 64-bit).
   - It has an executable stack. (Specifically, the `PT_GNU_STACK` program header has the executable `PF_X` flag set).
   - It contains `DT_RPATH` or `DT_RUNPATH` dynamic tags (which can be hijacked).
   
   A file is **compliant (clean)** if it is a valid 64-bit ELF and does not violate the above rules.
   You must implement this by parsing the ELF format directly in C (you may use `<elf.h>`). Do not use system calls to external commands like `readelf` or `objdump`.

3. **Multi-Service Integration**
   Start the services by running `/app/start_services.sh`. Ensure Nginx starts on port 8080, the backend on 9090, and Redis on 6379. 
   Verify that your end-to-end flow works: POSTing a binary to `http://127.0.0.1:8080/upload` should invoke your validator, log the audit trail to Redis, and return HTTP 200 (if clean) or 400 (if evil).

Your compiled binary `/home/user/elf_validator` will be evaluated against two corpora: 
- An "evil" corpus containing non-compliant files.
- A "clean" corpus containing compliant files.
Your validator must reject 100% of the evil corpus and accept 100% of the clean corpus.