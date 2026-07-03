You are a web security engineer tasked with rewriting a critical piece of our infrastructure. We have an existing Web Application Firewall (WAF) and URL router that validates requests, enforces rate limits, and resolves microservice dependencies before proxying requests. Currently, this logic is locked inside a slow, legacy stripped binary. 

We need you to implement a new, highly optimized version in C that perfectly matches the legacy binary's behavior but runs significantly faster.

Here are the details of the environment and your objectives:

1. **Configuration and Patching**:
   - You will find a base configuration file at `/app/routes_base.conf` defining the initial API endpoints and their dependency graphs.
   - We have a recent security update in the form of a patch file at `/app/security_update.patch`. Apply this patch to the base configuration to generate the final `routes.conf` file in your home directory (`/home/user/routes.conf`).

2. **The Oracle**:
   - The legacy stripped binary is located at `/app/legacy_waf_oracle`.
   - It takes the path to the configuration file as its first argument, and reads a stream of incoming HTTP request metadata from `stdin`.
   - Each input line is formatted as: `[Timestamp] [IP_Address] [HTTP_Method] [URL_Path]`
   - It outputs routing decisions to `stdout`, one per line, formatted as: `[IP_Address] [URL_Path] -> [ACTION]`. The `[ACTION]` is either `ROUTED_TO_<SERVICE>`, `DENIED_RATE_LIMIT`, or `DENIED_INVALID_ROUTE`.

3. **Your Implementation**:
   - Write a C program at `/home/user/fast_waf.c`.
   - Your program must implement the same URL routing, dependency resolution, and rate limiting logic as the oracle.
   - **Routing logic**: Parse the URL, match it against the configured endpoints in `routes.conf`.
   - **Rate Limiting**: Deduce the rate limiting mechanism and limits by experimenting with the oracle. (Hint: It uses a standard token bucket or fixed window approach per IP).
   - Compile your program to an executable named `/home/user/fast_waf`. Your program should accept the same command-line arguments and input/output formats as the oracle.

4. **Verification**:
   - Your C program must produce the exact same routing and rate-limiting decisions as the oracle for any given stream of requests.
   - Your program must be highly optimized. Our automated tests will measure both accuracy and execution speed.

To finish the task, ensure your source code is at `/home/user/fast_waf.c` and the compiled binary is at `/home/user/fast_waf`. Generate a test log by running your binary against a sample input of your choice and saving the output to `/home/user/test_run.log`.