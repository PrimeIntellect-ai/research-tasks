You are a web developer tasked with optimizing and implementing a custom routing and rate-limiting backend feature. The system uses a proprietary configuration language and requires high performance.

Your objective is to complete the following tasks in `/home/user`:

**1. Build System & Linking**
There is a C source file located at `/home/user/src/filter.c`. 
Write a `Makefile` in `/home/user` with the following targets:
- `build`: Compiles `src/filter.c` into a shared library named `libfilter.so` in `/home/user/`.
- `run`: Executes the Python scripts created in the next steps (in order: parser, then rate limiter).
- `bench`: Runs the rate limiter script using `/usr/bin/time -v` and redirects the output to `/home/user/benchmark.log`.
- `all`: Runs `build`, then `run`.

**2. State Machine Parser & Structured Data**
The routing configuration is located at `/home/user/route.conf`. It uses a custom markup.
Write a Python script `/home/user/parse_routes.py` that reads `route.conf` using a state-machine approach (iterating line-by-line, tracking state like `OUTSIDE`, `INSIDE_ROUTE`).
Convert the configuration into a JSON array and write it to `/home/user/routes.json`.
*Format mapping example:*
```
<route /api/v1/auth>
method POST
limit 3
</route>
```
*Maps to JSON:* `[{"path": "/api/v1/auth", "method": "POST", "limit": 3}]`

**3. Request Validation & Rate Limiting**
Write a Python script `/home/user/rate_limit.py` that processes an access log at `/home/user/requests.log`. 
- First, load the shared library `libfilter.so` using Python's `ctypes`. The C library contains a function `int is_valid_ip(const char* ip)`. Skip any log lines where the IP is invalid (function returns 0).
- For valid IPs, load the rules from `/home/user/routes.json`.
- Implement a rolling-window rate limiter. An IP should be marked as banned if it exceeds the `limit` for a specific `path` within **any 60-second window**. (The log file timestamps are integer Unix epochs).
- Output the list of banned IPs to `/home/user/banned_ips.txt` (one IP per line, sorted alphabetically).

Ensure all files are created with the exact names and paths specified. Your solution must be runnable via the `Makefile`. You do not need root access.