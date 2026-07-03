You are a mobile build engineer maintaining a data processing pipeline for a mobile app's asset management system. Part of the pipeline relies on a legacy C utility that parses asset manifest files, but it currently suffers from a memory safety issue (undefined behavior/buffer overflow). 

Your task consists of three parts:

1. **Repair the C Utility:**
   There is a C file at `/home/user/manifest_parser.c`. It reads an asset manifest and prints the parsed asset type and size. However, it crashes or causes undefined behavior when encountering long asset names due to a hardcoded buffer size, and it leaks memory. 
   Fix the C code so that it safely handles asset names up to 256 characters without buffer overflows, properly null-terminates strings, frees all allocated memory, and exits cleanly.

2. **Data Processing Script (Bash):**
   Create a script at `/home/user/process_assets.sh` that compiles the C utility and orchestrates the data processing. 
   - Compile the fixed `manifest_parser.c` to an executable named `parser` in the same directory using `gcc`. Include the `-fsanitize=address` flag to ensure your memory fixes are working.
   - Run the compiled `parser` on all `.txt` files located in `/home/user/manifests/`.
   - The output of the `parser` will be lines in the format: `ASSET: <Type> <Size>`.
   - Use a Bash associative array (custom data structure) to aggregate the total size of assets for each `<Type>`.
   - Write the aggregated totals to `/home/user/summary.log`.

3. **Output Format:**
   The final `/home/user/summary.log` must be sorted alphabetically by the asset `<Type>` and formatted exactly like this:
   ```
   [Type1]: [TotalSize1]
   [Type2]: [TotalSize2]
   ```

**Initial Setup Assumptions:**
- The directory `/home/user/manifests/` exists and contains several text files with manifest data.
- The buggy source code is located at `/home/user/manifest_parser.c`.

Ensure your Bash script is executable (`chmod +x /home/user/process_assets.sh`) and that running it produces the correct, aggregated `/home/user/summary.log` without any ASAN (AddressSanitizer) errors.