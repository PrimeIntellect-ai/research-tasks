You are a QA engineer tasked with migrating our testing environment off a legacy proprietary testing tool. 

We have a legacy tool located at `/app/legacy_chksum_bin` (a stripped binary). This tool is a simple bytecode interpreter used to validate data streams and their custom checksums. Because this binary is old and causing issues in our CI/CD pipeline, we need a pure Bash equivalent that produces the exact same output.

Your task is to write a pure Bash script at `/home/user/bash_parser.sh` that perfectly emulates this binary.

### Bytecode Specification
The tool takes a single command-line argument: a continuous hexadecimal string representing the bytecode (e.g., `011A0304052BFF`).
The virtual machine has a single 8-bit unsigned accumulator (initialized to `0x00`). All arithmetic strictly wraps at 8 bits (modulo 256).

Opcodes:
*   `01 <hex>`: ADD `<hex>` (1 byte) to the accumulator.
*   `02 <hex>`: SUBTRACT `<hex>` (1 byte) from the accumulator.
*   `03`: SHIFT LEFT the accumulator by 1 bit (equivalent to accumulator * 2, modulo 256).
*   `04`: XOR the accumulator with `0xA5`.
*   `05 <hex>`: CHECKSUM VERIFY. If the accumulator equals `<hex>`, print `OK\n`. Otherwise, print `FAIL\n`. Do not halt.
*   `FF`: HALT. Print `FINAL: <hex_value>\n` (where `<hex_value>` is the 2-character, zero-padded, uppercase hex of the accumulator) and immediately exit.

If the bytecode ends without an `FF` instruction, the program should just exit implicitly without printing the `FINAL: ...` line.
If an opcode requires an operand but the string ends prematurely, ignore the incomplete instruction and exit.

### Benchmarking Requirement
To ensure our test pipelines won't time out, we also need to benchmark your Bash implementation against the legacy binary.
Create a script at `/home/user/benchmark.sh` that:
1. Generates 50 random valid hex payloads (each between 10 and 30 bytes long).
2. Measures the total real execution time to run `/app/legacy_chksum_bin` sequentially over all 50 payloads.
3. Measures the total real execution time to run `/home/user/bash_parser.sh` sequentially over all 50 payloads.
4. Appends a report to `/home/user/benchmark_results.log` in the format:
   `Legacy: <time_in_seconds>s | Bash: <time_in_seconds>s`

Your `bash_parser.sh` must precisely match the behavior, output, and exit status of the legacy binary for any valid arbitrary bytecode.