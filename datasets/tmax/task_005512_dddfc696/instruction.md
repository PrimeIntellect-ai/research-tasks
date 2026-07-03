I am in the process of migrating our legacy systems from Python 2 to Python 3. However, for our core mathematical evaluation utility, I have decided to eliminate the Python dependency entirely to avoid any future migration issues. 

We have a legacy Python 2 script located at `/home/user/legacy_calc.py`. This script acts as a simple Reverse Polish Notation (RPN) mathematical interpreter. It takes a single string of space-separated tokens, evaluates it using a stack, and prints the integer result.

Your task has two parts:

1. **Code Translation (Interpreter Implementation)**
   Translate the logic of `/home/user/legacy_calc.py` into a pure Bash script at `/home/user/calc.sh`.
   - The script must accept the RPN expression as its first and only argument (e.g., `./calc.sh "3 4 + 2 *"`).
   - It must implement a stack using Bash arrays to process the operations: `+`, `-`, `*`, `/` (integer division), and `%` (modulo).
   - It should print the final resulting integer to standard output.
   - Make sure `/home/user/calc.sh` is executable.

2. **CI/CD Pipeline Setup**
   Write a lightweight test pipeline script at `/home/user/test_pipeline.sh` to verify your new Bash calculator.
   - The pipeline script should read test cases from `/home/user/test_cases.tsv`. 
   - The TSV file contains two tab-separated columns: `expression` and `expected_output`.
   - For each line in the TSV, the pipeline should execute `/home/user/calc.sh` with the expression.
   - If the output matches the expected output for all test cases, the pipeline must write the exact string `PIPELINE SUCCESS` to `/home/user/pipeline.log`.
   - If any test case fails, it should write `PIPELINE FAILED` to `/home/user/pipeline.log` and exit with a non-zero status.
   - Make sure `/home/user/test_pipeline.sh` is executable and run it once to generate the log.

Ensure your Bash translation correctly handles negative numbers and basic Bash arithmetic expansion limits (which are sufficient for these test cases).