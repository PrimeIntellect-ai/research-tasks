You are tasked with porting a legacy mathematical tool into a reliable microservice for a minimal container environment. 

We have a legacy mathematical expression evaluator located at `/app/v1_calc`. It is a stripped C binary that accepts Reverse Polish Notation (RPN) expressions via command-line arguments (e.g., `/app/v1_calc 5 4 + 2 *`).
However, this legacy binary has two major issues:
1. It has a known memory leak.
2. It crashes (segfaults) when a division by zero occurs.

Your task is divided into two parts:

**Part 1: Memory Profiling**
Analyze the memory leak in `/app/v1_calc` using `valgrind`. 
Run the binary with the arguments `10 5 +` under `valgrind`. Extract the exact number of bytes reported as "definitely lost" and save ONLY this integer to `/home/user/leak_report.txt`.

**Part 2: Bash Interpreter & Network Service**
Because the legacy binary is unstable, we cannot use it for our production network service. You must implement a pure Bash RPN interpreter and expose it as a TCP service.

Create a script at `/home/user/server.sh` that does the following:
1. Listens on TCP port `9000` (you may use `socat` or `nc`).
2. Accepts incoming line-based TCP connections. 
3. For each incoming line, parse and evaluate it as an RPN expression.
4. Supported operators are `+`, `-`, `*`, and `/`. All calculations should use standard Bash integer arithmetic.
5. If the evaluation is successful, reply with `RESULT: <value>\n` (e.g., `RESULT: 18`).
6. If the expression attempts to divide by zero, catch it before it happens and reply with `ERROR: DIV0\n`.
7. Handle multiple sequential or concurrent connections robustly.

Ensure your script `/home/user/server.sh` is executable and left running in the background, or provide instructions/ensure it starts when executed, as the automated verifier will test the live service on `127.0.0.1:9000`.