You are tasked with migrating a legacy mathematical evaluator tool from Python 2 to Python 3. The original Python 2 source code was lost, but we have a compiled Linux binary of the old tool located at `/app/oracle_bin`. 

The tool processes a custom serialized payload containing a math operation. Your goal is to write a Python 3 CLI program at `/home/user/evaluator.py` that is bit-for-bit identical in its output behavior to `/app/oracle_bin` for any valid or invalid input.

The CLI takes a single base64-encoded argument:
`python3 /home/user/evaluator.py <base64_payload>`

We found a scan of the original developer's whiteboard notes regarding the serialization format and parsing state machine. It is located at `/app/format.png`. You must analyze this image (e.g., using `tesseract`) to understand the exact custom header string, opcodes, and data format required to parse the payload. 

The payload roughly consists of:
1. A magic header string (detailed in the image).
2. A 1-byte opcode representing the mathematical operation (detailed in the image).
3. A 2-byte integer `L` (big-endian) denoting the length of the payload data.
4. `L` bytes of ASCII data containing a space-separated list of integers.

The tool must:
- Decode the base64 argument.
- Validate the magic header. If it does not match exactly, print "ERROR: INVALID_HEADER" and exit with code 1.
- Parse the opcode. If it is unknown, print "ERROR: UNKNOWN_OPCODE" and exit with code 1.
- Read the length `L` and extract the sequence of integers.
- Apply the mathematical operation (from left to right) to the integers.
- Print the final integer result to standard output and exit with code 0.

Write the `/home/user/evaluator.py` script. It must perfectly replicate the behavior of `/app/oracle_bin`, including all error messages and mathematical logic, so that an automated fuzzer comparing the two programs passes perfectly.

Ensure your program has execution permissions (`chmod +x /home/user/evaluator.py`) and includes the appropriate shebang (`#!/usr/bin/env python3`).