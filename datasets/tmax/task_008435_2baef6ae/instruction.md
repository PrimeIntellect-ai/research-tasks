I've recently inherited an old C codebase that parses text-based log files. The tool is supposed to read all `.log` files in a directory and extract event information. 

However, it currently crashes with a Segmentation Fault when I run it on the production logs provided in `/home/user/logs/`.

The source code for the tool is located at `/home/user/log_tool/parser.c`. You can compile it using the provided `Makefile` in the same directory (just run `make`).

Your task:
1. Debug `parser.c` to identify why it is crashing. The crash is caused by an edge-case in the log formatting that the original developer did not anticipate.
2. Fix the code. If a log line has an `EVENT:<TYPE>` but is missing the subsequent space and message payload, your fixed code should still parse the type, but output `(none)` for the message. 
3. Recompile the tool.
4. Run the tool against the `/home/user/logs/` directory.
5. Save the standard output of the successful run to `/home/user/fixed_output.txt`.

The output format printed by the program (and saved to your text file) must exactly match this structure for every valid event line found in the logs:
`File: [filepath], Type: [type], Msg: [message]`

If the message is missing (the edge case causing the crash), it must print:
`File: [filepath], Type: [type], Msg: (none)`