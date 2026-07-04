You are an IT support technician. A critical ticket has been escalated to you regarding a custom internal log processing tool located in `/home/user/log_tool`. 

The original developer has left the company, and the tool currently fails to compile. The only clue we have is a screenshot attached to the original ticket, located at `/app/ticket_attachment.png`, which shows the terminal output of the linker error. 
1. Analyze the image to determine the missing dependency or linker flag.
2. Fix the `Makefile` in `/home/user/log_tool` so that the tool compiles successfully.

Once compiled, users report that the `parser` binary sometimes hangs indefinitely (an iterative convergence failure) or crashes when processing raw logs from specific applications. It seems to happen intermittently depending on the specific formatting of the log messages.

Your primary goal is to write a Python sanitiser script at `/home/user/filter.py`. 
This script must take a single command-line argument (the path to a log file) and print to standard output only the lines that are "safe" for the C++ tool to process. Any line that would trigger the infinite loop, crash, or convergence failure in the C++ tool must be silently dropped. 

You can find some sample raw logs in `/home/user/samples/` to reproduce the intermittent failures and perform data transformation diff analysis on the C++ tool's output.

Requirements for `/home/user/filter.py`:
- Executed as: `python3 /home/user/filter.py <path_to_log_file>`
- Prints safe lines exactly as they appear in the original file (including trailing newlines).
- Drops malformed lines entirely.
- Do not print any extraneous debug information.

Your script will be tested against two hidden corpora of log lines: a set of purely clean logs, and a set of entirely malicious/malformed logs. To pass, your filter must retain 100% of the clean corpus and drop 100% of the evil corpus.