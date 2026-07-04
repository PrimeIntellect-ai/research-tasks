You are a support engineer investigating a bug in a critical diagnostic tool written in C. Customers are reporting that the newly compiled `diag-collector` tool outputs corrupted, inaccurate reports that crash their downstream parsing pipelines.

The source code for the tool is located in a local Git repository at `/home/user/diag-collector`. 

Your senior engineer left you the following notes about the ongoing issues:
1. **Missing Secret:** In a recent refactor, someone scrubbed a hardcoded calibration factor (a float value) from the code to improve security. However, they didn't provide the key to the support team! You need to dig into the repository's git history, find the original float calibration factor, and write it to a file exactly at `/home/user/secret.key`.
2. **Formula Precision Loss:** The new refactored C code reads the secret from the file, but the math formula is suffering from severe precision loss. The calculation is supposed to accurately apply the calibration factor and divide by 7.0, but it is currently truncating values due to integer conversion.
3. **Serialization Corruption:** The downstream pipeline expects exactly 5 `float` values (20 bytes) in the binary output file. However, an off-by-one boundary condition in the serialization loop is causing the tool to write out garbage data at the end of the file.

Your objective:
1. Recover the secret from the git history and save it to `/home/user/secret.key`.
2. Fix the bugs in `/home/user/diag-collector/main.c` (precision loss and off-by-one error).
3. Recompile the program (e.g., `gcc main.c -o collector`).
4. Run the program to generate the output file at `/home/user/diagnostic_report.bin`.
5. Encode the resulting binary file into Base64 format and save the base64 string to `/home/user/report.b64`.