You are tasked with developing a configuration patch validator for our custom Configuration Manager. Incoming configuration patches are received as custom-compressed binary files, and we need a C++ program to filter out invalid or malicious patches before they are applied.

First, locate the policy image at `/app/policy.png`. This image contains the latest validation rules text. You will need to extract the text from this image (e.g., using `tesseract`) to know the specific policy constraints your program must enforce.

The configuration patches are compressed using a custom Run-Length Encoding (RLE). The format is a sequence of byte pairs: `[count][character]`. For example, a byte with value `0x03` followed by `0x41` ('A') expands to "AAA".

Write a C++ program at `/home/user/config_filter.cpp` and compile it to `/home/user/config_filter`. 
Your program must accept exactly one command-line argument: the path to the configuration patch file to test.

Your program must perform the following:
1. **File Locking**: To prevent concurrent read issues in our pipeline, your program must first attempt to acquire an exclusive lock on the file `/tmp/config_filter.lock` (create it if it doesn't exist) using POSIX `flock` or `fcntl`. If it cannot acquire the lock immediately, it should exit with code 1.
2. **Custom Decompression**: Read the input file and decompress the custom RLE format in memory.
3. **Character Encoding / Content Validation**: The decompressed text must be parsed as standard ASCII. 
4. **Policy Enforcement**: Apply the rules you extracted from `/app/policy.png` to the decompressed text.
5. **Output**: 
   - If the patch is completely valid according to the custom compression format, encoding rules, and policy constraints, exit with code `0`.
   - If the patch violates any rule, fails decompression, or contains forbidden elements, exit with code `1` (or any non-zero exit code).

To test your implementation, we have provided two directories containing sample patches:
- `/app/corpus/clean/`: Contains valid patches that your program MUST accept (exit code 0).
- `/app/corpus/evil/`: Contains invalid, malicious, or poorly-formatted patches that your program MUST reject (non-zero exit code).

Ensure your compiled executable is located precisely at `/home/user/config_filter` and can be invoked as `/home/user/config_filter <path_to_patch>`.