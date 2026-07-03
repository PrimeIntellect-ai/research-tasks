You are tasked with organizing and filtering project configuration files for a distributed system. We allow users to upload JSON configuration files, but we need a strict filter to ensure they don't include malicious execution directives. 

We have a vendored copy of the `cJSON` C library located at `/app/cJSON-1.7.17`. Unfortunately, a previous developer accidentally broke the `Makefile` while trying to configure the build environment, so it currently fails to compile.

Your task consists of two parts:

1. **Fix and Build the Vendored Package:**
   Inspect the `Makefile` in `/app/cJSON-1.7.17` and fix the deliberate perturbation that is preventing compilation. Once fixed, build the static library `libcjson.a`.

2. **Write a Configuration Verifier:**
   Write a C program at `/home/user/verifier.c` and compile it to an executable at `/home/user/verifier`. Your program must link against the `libcjson.a` you just built.
   
   The executable must accept exactly one command-line argument: the absolute path to a JSON file.
   Usage: `/home/user/verifier <path_to_json_file>`
   
   The program must read the file (using standard C File I/O) and parse it using `cJSON_Parse`. It must then recursively traverse the parsed JSON structure to check for the presence of a forbidden key.
   
   **Rules for the Verifier:**
   - If the file cannot be read, is not valid JSON, or if the JSON tree (at any nesting level) contains a JSON Object with the exact key `"exec_cmd"`, the program must print `REJECT` to standard output and exit with status code `1`.
   - If the file is valid JSON and does *not* contain the key `"exec_cmd"` anywhere, the program must print `ACCEPT` to standard output and exit with status code `0`.

To successfully complete the task, your `/home/user/verifier` binary must be compiled, ready to run, and strictly adhere to the exit code and output requirements. We will test it against a hidden corpus of clean and malicious JSON files.