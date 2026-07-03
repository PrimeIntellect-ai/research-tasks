You are a performance and systems engineer tasked with fixing a custom math calculation server. 

We have an old proprietary service running as a stripped binary at `/app/math_oracle`. You can run it directly; it takes a single integer argument and prints a calculated result to stdout. 

We are rewriting this service in C++ to act as a high-performance TCP server. The source code is in a Git repository located at `/home/user/math_server`. However, the current `HEAD` of the repository is broken. It suffers from two major issues:
1. It frequently crashes with a segmentation fault (core dump) due to a recursion depth/loop termination bug when processing certain inputs.
2. Even when it doesn't crash, the mathematical formula implemented in the latest commit is incorrect and its outputs do not match the `/app/math_oracle` for inputs like `n=5` or `n=10`.

Your objectives are:
1. Use the `/app/math_oracle` to understand the correct expected output sequence.
2. Use `git bisect` in `/home/user/math_server` to identify the exact commit hash that introduced the formula logic regression (where the output stopped matching the oracle). Write the full 40-character commit hash of this bad commit to `/home/user/bad_commit.txt`.
3. Analyze the core dump behavior or stack trace of the latest commit to identify the recursion/loop termination bug.
4. Fix `server.cpp` so that it uses the correct formula, terminates properly for all non-negative integers without crashing, and performs efficiently.
5. Compile your fixed C++ server.
6. Start your fixed server so that it listens on `127.0.0.1:8080`. The server must accept raw TCP connections. When a client sends an integer followed by a newline (e.g., `5\n`), the server must respond with the correct calculated integer followed by a newline (e.g., `11\n`) and keep the connection open for further queries.

Leave the fixed server running in the background. Do not modify the original `/app/math_oracle` binary.