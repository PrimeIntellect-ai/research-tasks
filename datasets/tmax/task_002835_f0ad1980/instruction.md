You are an engineer investigating a legacy data processing service. We have a compiled data extraction tool located at `/app/log_parser`. Unfortunately, the source code is lost, and the binary has several critical issues:

1. **Memory Leak / Crash:** It leaks memory rapidly and will crash if it processes more than 20 lines of input in a single execution.
2. **Corrupted Input Handling:** If it encounters a line containing the exact string `CORRUPT`, it enters an infinite loop and hangs forever.

We need to safely expose this tool over the network so other services can use it without triggering its bugs.

Your task is to write a Bash-based TCP server that safely wraps this binary. 

Requirements:
1. Create a Bash script at `/home/user/server.sh`.
2. The script must listen for incoming TCP connections on `127.0.0.1:8000`. You may use `socat` or `nc` (socat is highly recommended for handling concurrent connections and EOF properly).
3. When a client connects, it will send a stream of newline-separated text lines, followed by EOF (the client will half-close the connection).
4. Your script must read the input and sanitize it by completely discarding any line that contains the word `CORRUPT`.
5. Your script must feed the sanitized lines to `/app/log_parser` via stdin. 
6. To circumvent the memory leak, your script must chunk the input: start an instance of `/app/log_parser`, feed it at most 10 lines, read its output, and then start a new instance for the next batch of up to 10 lines.
7. Send the concatenated output from all `/app/log_parser` executions back to the TCP client, then close the connection.

The binary `/app/log_parser` reads lines from stdin, processes them, and outputs exactly one line per input line to stdout.

Start your server in the background before finishing the task. We will verify your solution by connecting to `127.0.0.1:8000` and sending a test payload containing both clean and corrupted data spanning more than 20 lines.