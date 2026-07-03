You are helping a developer migrate a legacy log processing system from Python 2 to Python 3. 

The system receives log entries formatted as URLs, routes them to a simple expression evaluator based on the URL structure, and outputs the results in a format resembling a gRPC protobuf text message.

In `/home/user/`, you will find:
1. `legacy_parser.py`: A Python 2 script that reads URLs from standard input, parses the query parameters to extract mathematical expressions (e.g., `add(a,b)` or `sub(a,b)`), evaluates them using a basic custom interpreter, and prints a formatted result block.
2. `data.txt`: A file containing a list of log entries (some of which are valid `emu://` URLs).

Your task is to:
1. Create a new Python 3 compatible script at `/home/user/modern_parser.py`. It must have the exact same logic and output formatting as the legacy Python 2 script but must be fully compatible with Python 3. (You will need to update the standard library imports like `urlparse` and fix syntax changes like `print`).
2. Run your new `modern_parser.py` script using Python 3, passing the contents of `/home/user/data.txt` to its standard input.
3. Save the standard output of the script to a file named `/home/user/output.txt`.

Ensure that `/home/user/output.txt` exactly matches the expected protobuf-like text format. Do not include any extra output or debug information in `output.txt`.