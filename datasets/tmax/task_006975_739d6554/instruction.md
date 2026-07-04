You are an IT support technician acting as a Tier 3 Linux system debugger. We have received an escalated ticket (Ticket #9932) regarding a legacy data ingestion service that periodically crashes. 

The original developer has left the company, and unfortunately, the source code for the main parsing module (`parser.c`) was deleted. We only have the compiled object file `parser.o` and the main entry point source `main.c`. 

Our network team managed to capture the traffic sent to the service during one of the crash events. The service processes raw data from standard input (stdin).

Here are the files provided to you in `/home/user/ticket/`:
- `server`: The compiled, crashing executable.
- `main.c`: The source code of the main entry point, which calls `parse_and_process(char *input)` from the parser module.
- `parser.o`: The compiled object file of the missing parser module.
- `traffic.pcap`: A packet capture containing three distinct TCP streams directed at the server's port. One of the payloads in these streams triggers a buffer overflow.

Your task is to analyze the crash, reverse-engineer the deleted parser logic, and patch the service. 

Please produce the following deliverables in the `/home/user/solution/` directory (you must create this directory):

1. `/home/user/solution/crash_input.bin`: A raw binary file containing the exact payload extracted from `traffic.pcap` that causes the `server` to crash (segfault).
2. `/home/user/solution/fault_func.txt`: A plain text file containing exactly the name of the internal C function inside `parser.o` that is directly responsible for the buffer overflow (e.g., the function where the overflow occurs, not necessarily the exported function).
3. `/home/user/solution/safe_parser.c`: A newly written C source file that completely replaces `parser.o`. It must expose the `int parse_and_process(char *input)` function exactly as `main.c` expects. You must reverse engineer `parser.o` to understand its logic (it searches for a specific delimiter, copies the data after it, prints it, and returns the length) and reimplement it safely so that it truncates the copied data to 31 characters to prevent the buffer overflow.
4. `/home/user/solution/fixed_server`: A compiled executable created by compiling `main.c` with your new `safe_parser.c`. It must not crash when fed `crash_input.bin`, but must still correctly process the valid payloads.

Ensure all file paths and names match exactly. Do not use external libraries other than the standard C library.