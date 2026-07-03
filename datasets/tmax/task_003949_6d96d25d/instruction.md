You have inherited an unfamiliar C++ codebase from a developer who recently left the company. The codebase contains a custom binary log parser that extracts strings from memory dumps. However, the parser is currently broken: it crashes on certain inputs, fails to extract the correct strings, and runs incredibly slowly.

Before leaving, the previous developer left a screenshot of their notes at `/app/whiteboard.png`. You need to use the information in this image to configure the parser correctly.

Your objectives:
1. **Analyze the Image**: Read `/app/whiteboard.png` to find the correct `DELIM` (delimiter string) and `OFFSET` (number of bytes to skip after the delimiter before reading the string length).
2. **Update the Parser**: Modify `/home/user/parser/parser.cpp` to use the correct delimiter and offset.
3. **Fix the Crash**: The parser currently crashes with a segmentation fault due to a format parsing edge case (specifically, a malformed length byte causing a massive allocation or out-of-bounds read). Find and fix this bug.
4. **Performance Debugging**: The parser currently takes an unacceptably long time to process large files. Diagnose the bottleneck (hint: system call tracing might reveal inefficient I/O operations) and optimize the C++ code to run efficiently. 
5. **Extract Strings**: Compile your fixed code and run it on the provided memory dump `/app/mem_dump.bin`. The program should write the extracted strings to `/home/user/extracted_strings.txt`, one per line.

Requirements:
- The compiled binary must be located at `/home/user/parser/parser`.
- It must take the input file and output file as arguments: `./parser /app/mem_dump.bin /home/user/extracted_strings.txt`.
- **Performance Requirement**: Your optimized parser must execute in under 0.2 seconds.

You have full freedom to rewrite the I/O logic in C++ to achieve the performance target, but the output logic must faithfully extract the strings as defined by the binary format.