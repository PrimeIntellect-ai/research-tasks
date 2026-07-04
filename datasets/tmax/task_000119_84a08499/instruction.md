You are a mobile build engineer maintaining a CI/CD pipeline. One of the pipeline steps relies on a custom C utility, `manifest_parser`, to deserialize binary-like configuration files (key-value pairs) into JSON for downstream web services. Recently, security scans flagged this utility for memory safety vulnerabilities, and the pipeline is currently broken.

Your task is to fix the utility, repair the build system, and create a Bash wrapper to integrate it back into the pipeline.

You are working in the directory: `/home/user/pipeline/`

Here is what you need to do:
1. **Fix the Makefile (`/home/user/pipeline/Makefile`)**: The Makefile is broken and fails to compile the C program. Fix it so that running `make` correctly compiles `manifest_parser.c` into an executable named `manifest_parser`. Ensure you add the `-Wall` compiler flag.
2. **Fix Memory Safety in C (`/home/user/pipeline/manifest_parser.c`)**: The C code processes `payload.dat`. It currently has a severe buffer overflow vulnerability because it reads an unbounded string into a fixed-size buffer (32 bytes) for the `value` field during deserialization. The pipeline inputs can now have values up to 127 characters long. Update the C code to increase the `value` buffer size to 128 bytes and safely constrain the `fscanf` (or similar) reading mechanism so it never overflows, even with malicious inputs.
3. **Write a Bash Script (`/home/user/pipeline/process.sh`)**: Create a Bash script that does the following:
   - Compiles the code by running `make`.
   - Executes the compiled `./manifest_parser` passing `payload.dat` as the first argument.
   - Captures the standard output of the parser and saves it exactly to `/home/user/pipeline/output.json`.
   - Exits with a status code of 0.
   - Make sure the script is executable (`chmod +x`).

The file `payload.dat` contains a long malicious string designed to trigger the overflow. If your C code fix is correct, the parser will not segfault and will output valid JSON lines. 

Run your `process.sh` script to verify it works and generates `output.json`.