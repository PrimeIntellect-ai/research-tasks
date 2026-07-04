You are a build engineer managing legacy artifact processing. We have a pipeline that extracts configuration metrics embedded inside compiled binary artifacts, evaluates them, and logs the results.

However, the pipeline is broken due to a C tool crashing, and we need to orchestrate the extraction using a Python script.

Here is what you need to do:

1. **Fix the Extractor (C/C++ Memory Safety):**
   There is a C program located at `/home/user/build_tools/extractor.c`. Its purpose is to read an artifact file, find a block starting with `HEX[` and ending with `]`, and print the contents as `ENCODED:<data>`.
   Currently, it suffers from a memory safety issue (buffer overflow/missing null-terminator) that causes it to crash or output garbage when processing our artifacts. Identify the undefined behavior, fix the C code, and compile it using the provided `/home/user/build_tools/Makefile` (run `make` inside the directory).

2. **Process Artifacts (Polyglot Orchestration, Encoding & Evaluation):**
   Write a Python script at `/home/user/process_artifacts.py`. This script must:
   - Iterate over all `.bin` files in the `/home/user/artifacts/` directory.
   - For each file, run the fixed `/home/user/build_tools/extractor` binary.
   - Parse the standard output (which should look like `ENCODED:3130202b2035202a2032`).
   - The extracted data is a Hexadecimal encoded string. Decode it to standard ASCII text.
   - The decoded text will be a mathematical expression (e.g., `10 + 5 * 2`). Parse and evaluate this expression using standard mathematical order of operations. You can assume all evaluated results will be integers.
   
3. **Save the Output:**
   Your Python script must output the final evaluated results to a JSON file located at `/home/user/artifact_metrics.json`. 
   The JSON should be a flat dictionary mapping the base filename (e.g., `module_A.bin`) to its evaluated integer metric.

Ensure your Python script completely automates steps 2 and 3 when executed, and ensure the C program is safely compiled and correctly terminates strings without overflowing buffers.