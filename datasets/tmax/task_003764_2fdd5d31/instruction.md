You are a storage administrator managing a massive volume of highly sparse, repetitive binary log files. To save disk space efficiently without installing third-party tools, you need to write a custom C++ compression utility.

Your task is to write, compile, and execute a C++ program that implements a custom "Null-Byte Run-Length Encoding (RLE)" algorithm, reads from standard input, and safely writes to a file using atomic operations.

**Step 1: Create the Compression Utility**
Write a C++ program at `/home/user/null_compressor.cpp`. 
The program must adhere to the following strict requirements:
1. **Input:** It must read raw binary data from `stdin`.
2. **Arguments:** It must accept exactly one command-line argument: the absolute path to the desired output file.
3. **Atomic Writes:** To prevent data corruption if the process is interrupted, the program must open and write all output to a temporary file named by appending `.tmp` to the target output path (e.g., `<output_file>.tmp`). 
4. **Completion:** Only after successfully reading all data from `stdin` to EOF, and successfully closing the temporary file, the program must atomically rename the `.tmp` file to the final target `<output_file>` path.
5. **Compression Algorithm (Null-Byte RLE):**
   Process the input stream byte by byte.
   * **Rule 1:** If the byte is neither `0x00` nor `0xFF`, write the byte to the output exactly as-is.
   * **Rule 2:** If the byte is `0xFF`, write two bytes to the output: `0xFF` followed by `0x00`.
   * **Rule 3:** If a continuous sequence of null bytes (`0x00`) is encountered, count them. Write `0xFF` followed by the count $N$ as a single unsigned byte. Since a single byte can only represent up to 255, if the sequence has more than 255 nulls, output `0xFF` followed by `0xFF` (representing 255 nulls), and continue counting the remaining null bytes. 
   *(Example: 3 null bytes become `0xFF 0x03`. 256 null bytes become `0xFF 0xFF 0xFF 0x01`)*

**Step 2: Compile and Process**
1. Compile your code to the executable `/home/user/null_compressor` (e.g., using `g++ -O2`).
2. A raw binary file already exists at `/home/user/raw_data.bin`.
3. Process this file by streaming it into your compiled utility using shell piping, saving the output to `/home/user/compressed.archive`.
   Example execution pattern: `cat /home/user/raw_data.bin | /home/user/null_compressor /home/user/compressed.archive`

Ensure that your C++ code correctly handles binary streams (avoiding newline translations) and that `/home/user/compressed.archive.tmp` does not exist after a successful run.