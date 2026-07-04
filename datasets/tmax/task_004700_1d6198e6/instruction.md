We have a long-running Python service that processes incoming data streams. Recently, it has been crashing due to memory leaks and Out-Of-Memory (OOM) errors when processing certain large, malformed payloads.

You are provided with the following files:
1. `/home/user/leaky_parser.py` - The current Python parser. It reads a data string from stdin and prints the parsed output to stdout.
2. `/home/user/payload.txt` - A large data file containing a sequence of tokens that causes `leaky_parser.py` to memory leak and eventually crash.
3. `/app/oracle_parser` - A compiled reference binary that correctly parses data without leaking. Our goal is to make the Python parser behave exactly like this oracle.
4. `/app/protocol.png` - An image containing a snapshot of the legacy protocol rules. You may need to extract the text from this image to understand the expected parsing state machine.

Your objectives:
1. Run the parser with the provided payload to observe the memory leak.
2. Use delta debugging or test minimization techniques on `payload.txt` to isolate the exact malformed token sequence that triggers the infinite memory allocation.
3. Fix the logic in the Python parser so that it handles the edge case correctly without leaking memory.
4. Ensure your fixed parser perfectly matches the exact output of `/app/oracle_parser` for *any* input. You should write a fuzzing script to test your implementation against the oracle with random sequences of tokens.

Save your final corrected parser to `/home/user/fixed_parser.py`. It must accept input on stdin and print the exact parsed string to stdout, just like the oracle.