You are a penetration tester tasked with auditing a proprietary, closed-source authentication daemon.

The developers have provided a stripped version of the binary located at `/app/auth_daemon`. When executed, this binary listens on `127.0.0.1:8080`. 

Your objectives are as follows:
1. **Service Auditing & Reversing:** Analyze the `/app/auth_daemon` binary (using tools like `strings`, `objdump`, etc.) to understand its HTTP-like protocol. The service implements an internal "Content Security Policy" and WAF filter. You must discover the exact HTTP headers required to bypass this filter and receive a `200 OK` or `404 Not Found` response instead of a `403 Forbidden`.
2. **Exploit Crafting:** The daemon has a hidden vulnerability on its `/verify` endpoint. It accepts an integer `id` parameter (ranging from 0 to 20000). Only one specific `id` contains a memory leak that will return the system flag (format: `FLAG{...}`).
3. **High-Performance Implementation:** Write a Go program at `/home/user/audit.go` that targets the running daemon. Your Go program must dynamically scan the `id` parameter from 0 to 20000. Because the daemon drops connections sequentially over a certain limit, or simply because sequential scanning is too slow for our engagement, your Go program *must* be heavily concurrent. 

**Requirements for `/home/user/audit.go`:**
- It must inject the correct headers to bypass the internal network/CSP policy.
- It must find the vulnerable `id` and extract the flag.
- It must print *only* the exact flag string (e.g., `FLAG{...}`) to standard output and then exit.
- It must complete its execution extremely quickly. 

**Evaluation Metric:**
An automated verification system will run your Go program against a fresh instance of the daemon. Your solution will be evaluated based on execution time. To pass, your program must output the correct flag and complete the full execution in **under 1.0 seconds**. A naive sequential scan will fail this metric threshold.

To begin, start the daemon in the background:
`/app/auth_daemon &`
Then write your solution.