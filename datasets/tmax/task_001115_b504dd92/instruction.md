You have inherited an unfamiliar, undocumented C codebase for a custom network packet parser located in `/home/user/packet_parser`. The previous developer left abruptly, and the service is currently unusable due to a severe bug. Under certain conditions, when parsing malformed packet captures, the parser enters an infinite loop and rapidly leaks memory, simulating a resource exhaustion attack (similar to a thread leak under cancellation in concurrent services, but here it's an event-loop hang).

Your objective is to fully recover and repair this project. You must perform the following tasks:

1. **Git Forensics & Secret Recovery**: 
   The parser requires a 16-character hexadecimal "Master Key" to decrypt payload segments. The previous developer accidentally hardcoded this key into the source code in an early commit, but later removed it to "secure" the codebase. 
   - Dig through the git repository's history in `/home/user/packet_parser` to find this lost key.
   - Save the exact 16-character key string into a new file at `/home/user/secret_key.txt`.

2. **Format Parsing Edge-Case & Boundary Condition Repair**:
   The primary file `parser.c` contains a parsing loop for a custom TLV (Type-Length-Value) format. However, there is an off-by-one boundary condition or a missing length validation that causes an infinite loop when a specific malformed record (e.g., a zero-length chunk or out-of-bounds read) is encountered.
   - Identify and fix the bug in `parser.c`. You may write a quick fuzzing script in Python to generate malformed inputs to test the binary and isolate the hang if helpful.
   - The fixed C code must safely reject or skip malformed chunks without hanging or crashing.

3. **Compilation and Execution**:
   - Recompile the fixed `parser` using the provided `Makefile`.
   - Run the compiled binary on the provided capture file: `/home/user/packet_parser/data/capture.bin`. You will need to pass the recovered key to the program via command-line arguments (run `./parser -h` or read the source to see how).
   - Redirect the standard output of the successful, full parse of `capture.bin` to `/home/user/final_output.txt`.

**Deliverables:**
Make sure the following files exist and are correct before you finish:
1. `/home/user/secret_key.txt` (containing only the recovered 16-character hex key).
2. `/home/user/final_output.txt` (containing the parsed output of `capture.bin`).