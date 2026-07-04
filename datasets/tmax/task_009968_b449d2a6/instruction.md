As a web developer, you need to build a lightweight microservice to evaluate mathematical expressions. However, for a highly constrained environment, you must build the entire service and the mathematical interpreter using purely Bash. 

Your task has three parts:
1. **Mathematical Interpreter & REST API (Bash)**
   Create an executable Bash script at `/home/user/rpn_server.sh` that acts as an HTTP server listening on port `8080`. 
   - You may use `nc` (netcat) or `socat` to handle the socket binding, but the request parsing and mathematical evaluation MUST be written in Bash.
   - The server must handle incoming `GET` requests to the endpoint `/evaluate`.
   - The mathematical expression will be provided via a custom HTTP header: `X-Expr: <expression>`.
   - The expression will be in **Reverse Polish Notation (RPN)**, containing space-separated positive integers and the operators `+`, `-`, `*`, and `/`.
   - You must implement a custom stack-based RPN evaluator in Bash to compute the result. 
   - The server must return a valid `HTTP/1.1 200 OK` response with a `Content-Type: text/plain` header, and the response body must contain exactly the resulting integer followed by a newline.

2. **Performance Benchmarking**
   Create a benchmarking script at `/home/user/benchmark.sh`.
   - The script must make 50 sequential `curl` requests to your API endpoint.
   - For every request, use the exact RPN expression: `15 7 1 1 + - / 3 * 2 1 1 + + -`
   - Capture the integer response body from each request and append it to `/home/user/responses.txt` (so it should have 50 lines).
   - Use the `time` command (or similar) to measure the total wall-clock time it takes to complete all 50 requests. Write the total time (in seconds or milliseconds, format doesn't strictly matter as long as it represents the total duration) to `/home/user/benchmark_result.txt`.

Ensure your server is running in the background before executing the benchmark.

Constraints:
- Do not use external scripting languages (like Python, Perl, awk, bc, or Node.js) to evaluate the math expression. You must implement the RPN stack logic yourself using Bash built-ins (e.g., arrays and `$(( ))`).
- You can install system utilities like `socat` or `netcat-openbsd` using standard package managers if needed (assuming you have sudo privileges, or they might already be installed).

Verify your setup by running `/home/user/benchmark.sh` and ensuring both `/home/user/responses.txt` and `/home/user/benchmark_result.txt` are created and correctly populated.