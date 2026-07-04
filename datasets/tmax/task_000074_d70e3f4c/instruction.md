You are tasked with recovering and completing a legacy data processing pipeline. The system consists of multiple microservices, a C-based expression evaluator, and a Bash command-line utility. The environment contains a broken setup, and you need to fix the components and write a Bash utility that exactly matches the behavior of a missing production script.

Here is the current state of your workspace in `/home/user/workspace`:
1. **Database:** An SQLite database is used for logging. A migration script `migrate.sh` and a new schema file `v2_schema.sql` are present. You must apply this schema migration to `/home/user/workspace/data.db`.
2. **C Evaluator (Service C):** Located in `/home/user/workspace/c_eval/`. It listens on TCP port 5002, parses mathematical expressions, logs them to the database, and returns the result. The `Makefile` is currently broken (missing linker flags for sqlite3 and math library), and `eval.c` has a minor type mismatch bug on line 42. Fix the code, compile it, and start the service in the background.
3. **HTTP Proxy (Service B):** A Python service in `/home/user/workspace/proxy/` that translates HTTP REST requests on port 5001 to a custom binary protocol expected by Service C on port 5002. Start this service in the background.
4. **Nginx Router (Service A):** An Nginx configuration file is at `/home/user/workspace/nginx.conf`. It is supposed to route requests from `http://127.0.0.1:8080/compute` to the HTTP Proxy on port 5001. However, the configuration currently points to the wrong port. Fix the config and start Nginx using it.

**Your Final Objective:**
Write a purely Bash script at `/home/user/process.sh` that takes a single argument: a URL-encoded query string (e.g., `val1=10&val2=5&op=mul`). 
The script must:
1. Parse the query string to extract `val1`, `val2`, and `op` (which can be `add`, `sub`, or `mul`).
2. Construct a `GET` request to the Nginx router: `http://127.0.0.1:8080/compute?v1=<val1>&v2=<val2>&op=<op>` using `curl`.
3. Read the plain text integer response.
4. Output the exact string: `RESULT: <integer_response>` to standard output, followed by a newline.

Your script `/home/user/process.sh` must be executable (`chmod +x`). Once all services are running and your script is ready, an automated fuzzer will test your script with thousands of random inputs to ensure it behaves exactly like our reference implementation.