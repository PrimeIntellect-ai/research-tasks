You are helping a senior developer recover and organize a massive batch of proprietary streaming log files from a legacy system. The original parser for these files was lost, but we have a compiled reference binary and an architectural diagram that describes the protocol.

Your objective is to recreate the log parsing program in C, making sure it perfectly replicates the behavior of the reference binary.

### Step 1: Recover the Delimiter
An old architectural diagram is saved at `/app/system_diagram.png`. 
1. Use an OCR tool (like `tesseract`, which is pre-installed) to extract the text from this image.
2. Search the extracted text for a sequence in the format `DELIMITER: <8-CHARACTER-HEX>`. This represents the 4-byte magic sequence used to chunk the log files. 

### Step 2: Write the Log Parser (C)
Write a C program at `/home/user/log_parser.c` and compile it to an executable at `/home/user/log_parser`. 

**Requirements for the parser:**
*   **Invocation:** The program must accept exactly one command-line argument: the path to an input file. (e.g., `./log_parser /path/to/input.bin`).
*   **Memory-Mapped I/O:** The program **must** use `mmap` to map the input file into memory for high-performance reading. 
*   **Processing:** It must scan the mapped memory and write output to `stdout`. 
*   **Transformation:** All bytes should be passed through to `stdout` unchanged, *except* when the 4-byte magic sequence (discovered in Step 1) is encountered. The bytes appear in the exact order specified by the hex string (e.g., if the OCR reads `AABBCCDD`, the exact byte sequence is `0xAA`, `0xBB`, `0xCC`, `0xDD`).
*   **Splitting:** Whenever this 4-byte sequence is found, do NOT output the 4 bytes. Instead, output the exact ASCII string `[LOG_SPLIT]\n`.
*   **Summary:** After processing all bytes in the file, output a final summary line exactly formatted as `\nEOF_CHUNKS: <N>\n`, where `<N>` is the total number of times the delimiter was found and replaced. (If the file does not end with a newline naturally, the summary line still begins with `\n`).

### Step 3: Verification
We have a stripped reference binary (the oracle) located at `/app/oracle_parser`. 
The output of your `/home/user/log_parser` must be **bit-for-bit identical** to the output of `/app/oracle_parser` for ANY given arbitrary binary file. Our automated fuzzing suite will run thousands of random binary inputs through both your program and the oracle to verify they are perfectly equivalent. 

Test your program thoroughly against `/app/oracle_parser` using test files containing edge cases (empty files, files entirely composed of delimiters, files without delimiters, etc.) before finishing the task.