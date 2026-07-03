You are a developer tasked with debugging a custom forensics data extraction tool. The project is located in `/home/user/forensics_tool`. It is designed to parse a proprietary binary evidence file and extract a hidden payload. However, the current build is failing, and even when compiled, it hangs or produces incorrect output.

Your objectives are to diagnose and fix the following issues in the codebase:
1. **Linker Error:** The `Makefile` has a flaw preventing the project from building successfully. Fix the build process so that running `make` produces the executable `./carver`.
2. **Serialization Issue:** The tool reads a binary header struct, but it reads the fields incorrectly due to struct padding/alignment issues. Fix the definition of `struct EvidenceHeader` in `decoder.h` so it correctly maps to the packed binary format.
3. **Convergence Failure:** The function `find_sync_offset` in `decoder.c` attempts to find the end of the header using a custom iterative search algorithm. Currently, it gets stuck in an infinite loop (fails to converge) on certain data patterns. Fix the loop logic so it successfully converges and returns the correct offset.
4. **Boundary Condition:** The `extract_payload` function has an off-by-one error when processing the byte array, causing it to read past the buffer and corrupt the end of the decoded string. Correct the loop boundaries.

Once you have fixed the code:
1. Compile the tool by running `make`.
2. Run `./carver /home/user/data/evidence.bin`. It should now print a decoded flag to standard output.
3. Save the exact decoded flag into a file at `/home/user/extracted_flag.txt`.
4. Create a regression test script at `/home/user/test_runner.sh` (make it executable). This bash script should execute `./carver /home/user/data/evidence.bin`, capture the output, and exit with status code `0` if the output is correct, and `1` if the output is incorrect or the program fails.

Ensure all your fixes are applied directly to the files in `/home/user/forensics_tool`.