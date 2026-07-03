You are a security researcher analyzing a suspicious binary found on a compromised Linux system. 

We have recovered two key artifacts:
1. `/app/suspicious_parser.bin`: A compiled C executable (stripped) that reads a file and decodes a hidden payload.
2. `/app/intercepted_note.png`: An image of a handwritten note intercepted from the threat actor. It contains the "magic header" string required to activate the binary's parsing logic.

Initial analysis indicates:
* The binary requires an input file to be passed as the first argument (`/app/suspicious_parser.bin <input_file>`).
* If the input file starts exactly with the magic header (found in the PNG) followed by a newline (`\n`), the binary reads the rest of the file, applies a custom byte-level decoding algorithm, and prints the decoded payload to standard output.
* If the file does not start with the magic header, it prints "INVALID HEADER" and exits with status 1.
* The binary contains a severe vulnerability: a buffer overflow. If the payload following the magic header is larger than 64 bytes, the binary crashes and generates a core dump.

Your task:
Write a safe Python reimplementation of this parsing and decoding logic that does not crash on large payloads. 
Save your script at `/home/user/safe_parser.py`.

Requirements for `/home/user/safe_parser.py`:
- It must take a single command-line argument: the path to the input file to parse (`python3 /home/user/safe_parser.py <input_file>`).
- It must implement the exact same decoding algorithm as the C binary. You will need to use OCR to extract the magic header, trigger the crash in the binary (or use small payloads to observe the IO), and use tools like `gdb` or `strace` to analyze the binary/core dump to reverse-engineer the decoding loop.
- It must correctly process payloads of *any* length, completely avoiding the buffer overflow limitation of the original binary.
- It must print "INVALID HEADER" to stdout and exit with status code 1 if the magic header is incorrect.
- The output (stdout) for valid payloads must be bit-exact equivalent to what the original binary would output if its buffer were infinitely large.

Do not use any external APIs. Tools like `tesseract-ocr` and `gdb` are available in your environment.