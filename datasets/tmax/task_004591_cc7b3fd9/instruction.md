We are porting a legacy mathematical evaluation engine to run in a minimal containerized environment. The engine is written in C and evaluates Reverse Polish Notation (RPN) mathematical operations. However, the C code has memory safety issues, a buggy state machine in its parser, and a broken Makefile. 

Additionally, we need to wrap this C tool with a Bash-based TCP daemon that provides a caching layer using Redis, as we cannot deploy our standard heavy application servers in this environment.

Your objectives are:

1. **Repair the C Backend:**
   - Fix the Makefile in `/app/math_eval/Makefile` so it correctly compiles the executable `/app/math_eval/math_eval` from `main.c` and `eval.c`.
   - The C code in `/app/math_eval/eval.c` implements a custom stack data structure and a state machine parser. It suffers from memory leaks, undefined behavior (buffer overflows on the stack), and a logic bug in the parser state machine where it fails to correctly process the `MUL` instruction. Debug and fix these issues so that `math_eval` safely reads newline-separated RPN instructions from `stdin` and prints the final result to `stdout`.

2. **Develop the Bash TCP Server:**
   - Write a Bash script `/app/server.sh` that acts as a TCP server listening on port `8080`. You may use `socat` to handle the TCP listener.
   - For every incoming TCP connection, the server must read all incoming data until the connection is closed by the client (EOF).
   - The server must compute the MD5 hash of the received input string (ignoring trailing whitespace) to use as a cache key.
   - It must query the local Redis instance (listening on `127.0.0.1:6379`) using `redis-cli GET <key>`. 
   - If a cached result exists, send it back to the TCP client.
   - If no cached result exists, pipe the input into the fixed `/app/math_eval/math_eval` binary. Capture its standard output, store it in Redis using `redis-cli SET <key> <output>`, and then send the output back to the TCP client.
   - Ensure the server can handle multiple sequential connections.

Make sure `/app/server.sh` has executable permissions. You must leave the Redis server running and your Bash server running in the background when you complete the task.

**System State:**
- Redis is installed and running on `127.0.0.1:6379`.
- `socat` and `redis-cli` are available.
- All working files are located under `/app`.