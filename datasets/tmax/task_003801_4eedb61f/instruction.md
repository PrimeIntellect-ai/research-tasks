You are assisting a researcher in organizing a massive dataset of multi-line scientific sensor logs. The data ingestion pipeline requires a strict sanitization step to filter out corrupted or malicious "evil" records while perfectly preserving "clean" ones.

Here is your task:

1. **Fix the Vendored JSON Library**
   We rely on a local, pre-vendored copy of the `cJSON` C library to parse the records. It is located at `/app/vendored/cJSON-1.7.15`. 
   However, a colleague accidentally broke the build configuration in this repository. Identify the perturbation in its `Makefile` (or build scripts), fix it, and compile the library to produce a static archive (`libcjson.a` or equivalent).

2. **Develop the C Sanitizer**
   Write a C program located at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`.
   This program must statically link against your fixed `cJSON` library.
   
   The sanitizer must accept two command-line arguments:
   `./sanitizer <input_file> <output_file>`
   
   **Record Format:**
   The input files consist of multiple JSON objects, each representing a single sensor record. Each JSON object might span multiple lines, but they are separated by a special delimiter line exactly matching: `---END_RECORD---`
   
   **Sanitization Rules:**
   You must read the input file, parse each JSON block using `cJSON`, and write the exact original string of the JSON block (plus the `---END_RECORD---` delimiter) to the output file **ONLY IF** it meets all "clean" criteria:
   - The block is valid JSON (successfully parsed by `cJSON`).
   - It contains a string field `"type"` with the exact value `"sensor_reading"`.
   - If it contains a numeric field `"calibration_error"`, the value must be strictly `<= 5.0`. (If the field is missing, it is considered clean).
   
   Any record violating these rules must be discarded (omitted from the output file).

3. **Develop the Directory Processing Script**
   Write a shell script at `/home/user/pipeline.sh` that takes two arguments:
   `./pipeline.sh <input_dir> <output_dir>`
   
   The script must:
   - Recursively traverse `<input_dir>` to find all files ending in `.log`.
   - For each `.log` file, invoke your `/home/user/sanitizer` to process it.
   - Save the sanitized output in `<output_dir>` preserving the original relative directory structure and filename.

The automated verification suite will test your pipeline by pointing `./pipeline.sh` at hidden "clean" and "evil" dataset corpora. Your script and sanitizer must completely reject all evil records and perfectly preserve all clean records.