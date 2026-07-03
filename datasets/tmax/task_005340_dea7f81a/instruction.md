You are tasked with building a WebSocket routing and filtering utility for our internal API gateway. We have a multi-stage setup process that requires you to fix a broken Rust dependency, and then implement a Bash-based filter that evaluates URL routes against constraint rules.

**Stage 1: Fix the Vendored Package**
We use a small third-party Rust library to parse WebSocket URL paths into Bash-friendly associative arrays. The source code for this package is pre-vendored at `/app/ws-route-parser`.
Unfortunately, a recent patch introduced a Rust ownership and borrow-checker error in `/app/ws-route-parser/src/main.rs`.
- Identify and fix the borrow-checker error.
- Compile the binary using `cargo build --release`.
- The compiled binary will output parsed routing parameters in the format: `PATH=/api/v1/data ID=123 TOKEN=xyz`.

**Stage 2: Implement the Bash Filter**
Write a Bash script at `/home/user/ws_filter.sh`.
- The script will be invoked with a single argument containing a raw WebSocket URL request string (e.g., `/api/stream?room=42&user=admin`).
- Your script must use the compiled Rust binary (`/app/ws-route-parser/target/release/ws-route-parser`) to parse the URL.
- Translate the parsed route and parameters against a set of constraints. You must implement logic to satisfy the following constraints:
  1. The `PATH` must start with `/api/` or `/ws/`.
  2. If `PATH` contains `admin`, the `TOKEN` parameter must exist and be exactly 64 hexadecimal characters.
  3. The `ROOM` parameter (if present) must be an integer between 1 and 1000 inclusive.
  4. Block any request where the URL path contains `..` (directory traversal).
- The script must print `ALLOW` and exit with code 0 if the request satisfies all constraints.
- The script must print `DENY` and exit with code 1 if the request violates any constraint or fails to parse.

**Stage 3: Verification Against Corpora**
We have provided an adversarial corpus to test your filter's robustness.
- `/app/corpus/evil/`: Contains files with malicious or constraint-violating WebSocket URLs (one per file).
- `/app/corpus/clean/`: Contains files with valid WebSocket URLs.
Ensure your `/home/user/ws_filter.sh` perfectly rejects all evil inputs and accepts all clean inputs.