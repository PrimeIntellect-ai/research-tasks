You are taking over a partially organized project for a mathematical evaluation web service. The previous developer left a mess, and the service is currently broken and vulnerable. Your job is to fix, organize, and secure the application.

Here is the current state of the system:
1. **The Core Oracle**: There is a stripped legacy executable located at `/app/legacy_calc` that evaluates mathematical expressions. It is highly optimized but known to be vulnerable to buffer overflows and arbitrary code execution if given maliciously crafted mathematical strings.
2. **The Corpora**: In `/home/user/corpora/`, you will find two directories: `clean/` containing text files with valid, safe mathematical expressions, and `evil/` containing text files with malicious payloads disguised as math.
3. **The Project Directory**: `/home/user/project/` contains:
   - `filter.c`: An empty C file.
   - `service/`: A Rust web service (using `hyper` or similar standard library TCP bindings) that is supposed to act as a wrapper, calling the C filter via FFI.
   - `service/src/main.rs`: Contains a borrow-checker error in how it handles incoming TCP buffer streams.

Your objectives:
1. **Implement the C Filter**: Write the logic in `/home/user/project/filter.c` to act as a strict mathematical interpreter/sanitizer. It must read a string and return `1` if it is strictly valid math (only numbers, `+`, `-`, `*`, `/`, `(`, `)`, spaces, max 50 characters, balanced parentheses with a max nesting depth of 5), and `0` if it contains anything else. Compile this into a shared library `libfilter.so`.
2. **Fix the Rust Service**: Debug and fix the ownership/borrow-checker error in `/home/user/project/service/src/main.rs`.
3. **Polyglot Build Orchestration**: Write a `Makefile` in `/home/user/project/` that compiles the C shared library and builds the Rust service, linking them together correctly so the Rust service can call the `validate_math` C function.
4. **Reverse Proxy Configuration**: The Rust service runs on `127.0.0.1:3000`. Install and configure Nginx as a reverse proxy to expose this service on port `8080`. The Nginx configuration must reside at `/etc/nginx/sites-enabled/math_proxy` and Nginx must be running.

The final Rust executable must be located at `/home/user/project/service/target/release/math_service`. The service should accept an expression via a POST request to `http://127.0.0.1:8080/eval`, use the C library to validate it, and if valid, execute `/app/legacy_calc "<expression>"` and return the result. If invalid, return a 400 Bad Request.

Automated tests will verify the Nginx endpoint, compile your code using your Makefile, and directly run the adversarial and clean corpora against your C library and the web endpoint. Ensure 100% of the clean corpus is accepted and 100% of the evil corpus is rejected.