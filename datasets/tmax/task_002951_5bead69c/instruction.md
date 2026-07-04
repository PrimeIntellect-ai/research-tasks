You are acting as a release manager preparing a deployment pipeline that supports conditional cross-compilation based on target ABI versions.

Our build system dynamically generates CFLAGS based on the target system's GLIBC version. The exact mapping rules between the GLIBC version and the required build flags are documented in an image file located at `/app/abi_matrix.png`.

Your task is to write a Python script that takes a stream of target GLIBC versions and outputs the corresponding compilation flags. 

Requirements:
1. Create a Python script at `/home/user/generate_flags.py`.
2. The script must read from standard input (`stdin`). Each line of input will contain a single GLIBC version string (e.g., `GLIBC_2.28`).
3. The script must process each line and output to standard output (`stdout`) in the exact format:
   `TARGET <VERSION>: <FLAGS>`
   (e.g., `TARGET GLIBC_2.28: -D_MID_ABI -O2`)
4. If a provided version is NOT found in the `/app/abi_matrix.png` image, the script must output:
   `TARGET <VERSION>: UNKNOWN`
5. Extraneous whitespace in the output must be trimmed, but exactly one space must separate the colon and the flags.
6. The behavior of your Python script must be bit-for-bit identical to our legacy C-based reference oracle located at `/app/oracle_flags`. Your script will be tested against this oracle using an automated fuzzer with thousands of random inputs.

You may use standard Linux utilities (like `tesseract` for OCR, which is pre-installed) to inspect the image and hardcode the parsed mappings into your Python script, or your script can invoke OCR at runtime. However, a pre-parsed, hardcoded dictionary in your Python script is recommended for performance during the fuzzing phase.