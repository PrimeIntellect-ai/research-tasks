You are a QA engineer setting up a test environment for a new Web Security protocol parser. The development team needs a standalone C program to parse incoming protocol headers, enforce minimum version requirements, and support both a network-listening mode and a fuzz-testing mode.

Your task is to write the parser, compile it conditionally, and run a structured data test suite.

Step 1: Write the C Parser
Create a file at `/home/user/sec_parser.c`.
The program must read a single line of input (up to 256 characters) representing a protocol header.
Expected format: `SEC-PROTO V<major>.<minor>.<patch>`
Example: `SEC-PROTO V1.5.2`

Rules for the parser:
1. If the string does not strictly start with `SEC-PROTO V`, output exactly `[ERROR] Malformed prefix` and exit with code 1.
2. Extract the `<major>`, `<minor>`, and `<patch>` semantic version components as integers. If any component is missing or contains non-numeric characters (other than the periods separating them), output `[ERROR] Invalid version format` and exit with code 1.
3. Compare the parsed version to the minimum required secure version: `1.5.2`.
   - If the parsed version is strictly less than `1.5.2` (e.g., `1.5.1`, `1.4.9`, `0.9.0`), output `[REJECTED] Insecure version` and exit with code 2.
   - If the parsed version is greater than or equal to `1.5.2`, output `[ACCEPTED] Secure version` and exit with code 0.

Step 2: Conditional Build Logic
The C code must support a `FUZZ_MODE` preprocessor macro.
- If `FUZZ_MODE` is NOT defined, the program should prompt `Listening...` to standard output, read a single line from standard input, process it, and exit.
- If `FUZZ_MODE` IS defined, the program should NOT print `Listening...`. Instead, it should continuously read lines from standard input in a `while` loop until EOF is reached, processing and printing the result for each line without stopping on errors or rejections (ignore the exit codes in fuzz mode and just print the expected output string for each line, separated by newlines).

Step 3: Compilation
Compile the program twice:
1. Compile `/home/user/sec_parser.c` into an executable at `/home/user/sec_server` without any special flags.
2. Compile `/home/user/sec_parser.c` into an executable at `/home/user/sec_fuzzer` using the `-DFUZZ_MODE` flag.

Step 4: Property-Based Testing
Create a test input file at `/home/user/inputs.txt` containing exactly these 6 lines in this order:
SEC-PROTO V1.5.1
SEC-PROTO V1.5.2
SEC-PROTO V2.0.0
SEC-PROTO V1.4.99
SEC-PROTO V1.a.2
UNKNOWN V1.5.2

Run `/home/user/sec_fuzzer` with `/home/user/inputs.txt` fed into its standard input.
Redirect the standard output of this run to `/home/user/qa_report.log`.

Ensure all files are created exactly at the specified paths.