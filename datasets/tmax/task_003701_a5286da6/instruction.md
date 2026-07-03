You are a QA Engineer tasked with replacing a slow, legacy expression-evaluation component in our test environment with a fast C++ implementation, and wiring it up to our caching web-tier. 

Our current evaluation pipeline relies on three services:
1. An Nginx reverse proxy.
2. A Flask web server (which parses requests and calls a CLI evaluation tool).
3. A Redis cache.

Your objective is two-fold:

**Phase 1: Implement the Evaluator in C++**
Our legacy tool (`/app/oracle.py`) takes a Reverse Polish Notation (RPN) mathematical expression as a single command-line argument and prints the resulting integer to standard output. 
Write a C++ program at `/home/user/fasteval.cpp` that behaves EXACTLY like the legacy tool. 
- It must accept a single string argument containing space-separated tokens (e.g., `./fasteval "3 4 + 2 *"`) and print only the resulting integer.
- Supported operators: `+` (add), `-` (subtract), `*` (multiply).
- Operands: 32-bit signed integers.
- The output must be bit-exact identical to `/app/oracle.py` for any valid RPN expression.
- Compile your program to `/home/user/fasteval`. 

**Phase 2: Environment Configuration**
We need to wire up the test environment to use your new tool. 
The startup script `/app/start_services.sh` launches Nginx (using `/home/user/nginx.conf`), Redis (default port 6379), and the Flask app (`/home/user/app.py` on port 5000).
Currently, the configuration is broken or points to the legacy tool:
1. Modify `/home/user/nginx.conf` so that any HTTP GET requests to `http://127.0.0.1:8080/api/eval` are reverse-proxied to the Flask app on `http://127.0.0.1:5000/`.
2. Modify `/home/user/app.py` so that it calls your new compiled binary `/home/user/fasteval` instead of `/app/oracle.py`.
3. Fix the Redis caching logic in `/home/user/app.py` (which currently tries to connect to a dummy port 9999) to connect to the standard Redis port 6379. 

Ensure that if I run `curl "http://127.0.0.1:8080/api/eval?q=3%204%20%2B"` it returns `7`, caches the result in Redis, and uses your C++ binary.