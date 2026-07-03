You are an open-source maintainer reviewing a broken Pull Request. The PR aims to introduce a new fast-path C implementation for a mathematical and semantic-versioning Reverse Polish Notation (RPN) expression evaluator, which currently runs as a slow Python service. 

Currently, the services are organized as follows:
- **Nginx** is used as a reverse proxy. It is supposed to route `/api/v1/eval/legacy` to the existing Python Flask service running on port 5000, and `/api/v1/eval/fast` to the new C-based service running on port 5001.
- **Python Legacy Service** (`/app/legacy_service.py`) is the reference implementation.
- **C Fast Service** consists of a web server wrapper (`/app/fast_service.c`), the core interpreter (`/app/rpn_evaluator.c` and `/app/rpn_evaluator.h`), and a CLI wrapper (`/app/cli.c`).

The PR author left a few things broken:
1. **Nginx Configuration:** The file `/app/nginx.conf` has routing errors and is using the wrong upstream ports. You need to fix it so that it correctly routes the legacy and fast endpoints to ports 5000 and 5001 respectively.
2. **Interpreter Bugs:** The RPN core logic in `/app/rpn_evaluator.c` is flawed. The custom stack data structure has off-by-one errors in `push` and `pop`. Additionally, the semantic version comparison operators (`VER_LT`, `VER_GT`, `VER_EQ`) are currently implemented using raw string comparison (`strcmp`), which wrongly evaluates `"10.0.0"` as less than `"2.0.0"`. You must implement proper part-by-part semantic version comparison (Major.Minor.Patch).
3. **Property-based Parity:** The C evaluator must return the exact same integer results as the Python legacy evaluator for any valid RPN expression. 

Your tasks:
1. Fix the Nginx configuration in `/app/nginx.conf`.
2. Fix the stack implementation and semantic version comparison logic in `/app/rpn_evaluator.c`.
3. Compile the C CLI tool: `gcc -O3 /app/cli.c /app/rpn_evaluator.c -o /app/rpn_cli`. The CLI takes an RPN expression as its first argument and prints the resulting integer to stdout.
4. Compile the C web service: `gcc -O3 /app/fast_service.c /app/rpn_evaluator.c -o /app/fast_eval` (this requires `libmicrohttpd-dev` which is already installed).
5. Ensure that when all services are running, a request to `http://127.0.0.1:8080/api/v1/eval/fast?expr=<url_encoded_expr>` yields the exact same integer response as `http://127.0.0.1:8080/api/v1/eval/legacy?expr=<url_encoded_expr>`.

You do not need to start the background services permanently; an automated verifier will start Nginx, the Python service, and your compiled `/app/fast_eval` to verify end-to-end routing. It will also heavily fuzz your `/app/rpn_cli` against a secret reference binary to ensure bit-exact mathematical parity.