You are an integration developer testing a new backend processing binary that acts as a local mathematical API. The API is designed to consume serialized JSON arrays, compute the L2 norm (Euclidean norm) of the vector, and return a JSON object. 

You have been given the C source code for this backend tool in `/home/user/api_backend/process_data.c`. However, during load testing, the system has exhibited out-of-memory errors, and the backend engineers suspect a memory leak.

Your task consists of three phases: Memory Debugging, Patch Generation, and Integration Testing via Bash.

**Phase 1: Memory Debugging & Patch Generation**
1. Inspect `/home/user/api_backend/process_data.c`. Compile it into an executable named `process_data` in the same directory (ensure you include debugging symbols).
2. Use a memory profiling tool (like `valgrind`) to identify the memory leak in the C code.
3. Fix the memory leak in the C code.
4. Generate a standard unified diff patch file named `/home/user/api_backend/fix.patch`. This patch should contain the difference between the original buggy code and your fixed code. (You may want to save a copy of the original before editing).
5. Recompile your fixed `process_data` binary.

**Phase 2: Serialization & Numerical Implementation in Bash**
You must write an integration testing script at `/home/user/test_integration.sh`. This Bash script must perform the following:
1. Read a list of floating-point numbers (one per line) from `/home/user/input_data.txt`.
2. **Serialize** these numbers into a single JSON array string. The exact format required by the API is: `{"data": [num1, num2, num3]}`.
3. Pass this JSON string to the standard input of your compiled `./process_data` binary.
4. Capture the JSON output from the binary and **deserialize** it (using `jq` or shell utilities) to extract the computed L2 norm value.
5. **Numerical Algorithm**: Implement a Bash-native calculation (using `awk` or `bc`) within the script to compute the **L1 norm** (the sum of the absolute values) of the numbers in `/home/user/input_data.txt`.
6. Write the final results to `/home/user/integration_report.json` with the exact following JSON schema:
   ```json
   {
     "l2_norm_from_api": <extracted_value>,
     "l1_norm_from_bash": <calculated_value>
   }
   ```
   *(Ensure both values are represented as numbers, formatted to 4 decimal places).*

Ensure your Bash script `test_integration.sh` has executable permissions and is run at least once to generate `/home/user/integration_report.json` before you complete the task.