You are an integration developer responsible for building and testing the core backend engine for a new Mathematical API. The core engine is written in C for performance, and uses a custom string-serialized data structure called a "Fractional Vector" to avoid floating-point inaccuracies. 

The custom data structure is formatted as a string: `[Size] num1/den1 num2/den2 ...`
For example: `[3] 1/2 -3/4 5/1`

Your tasks are as follows:

1. **Patch the C Engine:**
   Navigate to `/home/user/vector_api/`. You will find the core C engine `vector_math.c` and a Makefile. 
   There is a known bug where the C engine fails to parse negative numerators properly because it uses `%u` instead of `%d` in `sscanf`. A colleague has provided a patch file named `negative_fix.patch`. Apply this patch to `vector_math.c`.

2. **Build the Shared Library:**
   Use the provided `Makefile` to compile the C code into a shared object file named `libvector.so`.

3. **Develop an Integration Test Script:**
   Write a Python script at `/home/user/vector_api/test_integration.py` that utilizes `ctypes` to interface with `libvector.so`. 
   The C library exposes the following function:
   `char* dot_product(const char* v1, const char* v2)`
   
   Your Python script must:
   - Read the test cases from `/home/user/vector_api/test_cases.json` (a dictionary mapping a `case_id` to an object with `v1` and `v2` strings).
   - Pass `v1` and `v2` to the `dot_product` C function.
   - Collect the returned string (the resulting fraction, which the C code automatically reduces to its lowest terms, e.g., `-1/4`).
   - *Important:* The memory returned by `dot_product` is heap-allocated by the C library. You do not need to free it for this short script, but you must ensure Python correctly interprets the returned `c_char_p`.
   - Save the results as a JSON file at `/home/user/vector_api/test_results.json`. The output JSON should be a flat key-value mapping of `case_id` to the result string.

Example expected output format for `test_results.json`:
```json
{
  "case1": "-1/4",
  "case2": "2/1"
}
```

Verify that your Python script runs without errors and produces the correct math results in `test_results.json`.