You are acting as a red-team operator simulating a defensive deployment. We have a web environment consisting of multiple services, but it is currently vulnerable to sophisticated open-redirect and SSRF evasion payloads.

Your objective is to create a custom Web Application Firewall (WAF) filter written in C that intercepts and analyzes incoming HTTP requests, effectively distinguishing between benign traffic and malicious evasion payloads.

Here is the setup:
The environment is orchestrated using a multi-service architecture located in `/app/`.
- Nginx is running on port 8080 as the front-end reverse proxy.
- A vulnerable Flask web server is running on port 5000 as the backend.
- A Redis instance is running on port 6379, used by the Flask app for session caching.

You are provided with two corpora of HTTP requests in `/app/corpus/`:
- `/app/corpus/evil/`: Contains raw HTTP requests with complex encoded payloads (e.g., URL encoding, hex encoding, mixed casing) designed to exploit the open redirect in the login flow.
- `/app/corpus/clean/`: Contains normal, benign HTTP requests from legitimate users.

Your tasks are to:
1. Audit the running services and their configurations in `/app/config/`.
2. Analyze the provided `payload_decoder.elf` binary in `/app/tools/` to understand how the backend processes and decodes incoming parameters.
3. Write a C program located at `/home/user/waf_filter.c` that compiles to `/home/user/waf_filter`.
4. Your `waf_filter` must act as a command-line classifier. It will take a file path as an argument (a raw HTTP request) and output exactly "CLEAN" or "EVIL" to stdout.
5. Reconfigure the Nginx setup to route traffic through your filter (optional for testing, but the primary verification will be against your compiled binary).

Your filter must:
- Reject (classify as "EVIL") 100% of the files in `/app/corpus/evil/`.
- Preserve (classify as "CLEAN") 100% of the files in `/app/corpus/clean/`.

Compile your C program with `gcc -o /home/user/waf_filter /home/user/waf_filter.c`. Ensure it handles the decoding logic necessary to identify the hidden payloads based on your ELF analysis.