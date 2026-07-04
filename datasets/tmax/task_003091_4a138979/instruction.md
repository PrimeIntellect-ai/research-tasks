As a QA engineer, I am setting up a test environment to validate our expression evaluation backend. I need a quick test fixture utility written in C to decode and evaluate test payloads, simulating the core logic of our REST API endpoint. 

Please create a C program and a build script with the following requirements:

1. Create a C program at `/home/user/evaluator.c`.
2. The program should read a single line of input from standard input (up to 100 characters). This input will be a hexadecimal-encoded string.
3. The program must first decode this hex string into standard ASCII characters. 
4. The decoded ASCII string will be a simple mathematical expression consisting of a positive integer, an operator (`+`, `-`, or `*`), and another positive integer (e.g., "12*5" or "100-42"). Parse and evaluate this expression.
5. The program should output the result to standard output strictly in the following JSON format: `{"status": "success", "result": <evaluated_number>}`. Make sure to print a newline at the end.
6. Create a bash script at `/home/user/build_and_test.sh` that:
   - Compiles `/home/user/evaluator.c` into an executable named `/home/user/evaluator` using `gcc`.
   - Reads the contents of `/home/user/payload.txt` and pipes it into the compiled `/home/user/evaluator`.
   - Saves the standard output of the evaluator to `/home/user/test_result.json`.

Ensure your bash script is executable. You can assume that `/home/user/payload.txt` is already present in the environment and contains a valid hex-encoded string. Run your bash script to generate the final `test_result.json` file.