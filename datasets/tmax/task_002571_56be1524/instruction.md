I am migrating an old data processing pipeline from Python 2 to Python 3. The pipeline consists of a Python script that reads CSV data and passes it to a custom command-line interpreter written in C.

The files are located in `/home/user/pipeline/`:
- `calc_interp.c`: A C-based interpreter that takes an operator (`+`, `-`, `*`) and two integers as arguments, and prints the result.
- `run_data.py`: A Python 2 script that parses `data.csv` and invokes the C interpreter.
- `data.csv`: A comma-separated file containing the operations.

I need you to do the following to complete the migration and set up a basic CI step:

1. **Fix the C Interpreter**: There is a logical bug in `calc_interp.c` where the addition operator `+` actually performs subtraction. Fix this bug in the C code so it correctly adds the two numbers.
2. **Migrate the Python Script**: Update `run_data.py` so that it is fully compatible with Python 3. You can modify the file in place. Ensure it correctly decodes the stdout from the C interpreter and prints the exact string format.
3. **Create a CI Pipeline Script**: Write a bash script at `/home/user/pipeline/ci_build.sh` that automates the build and test process. The script MUST:
   - Be executable.
   - Compile `calc_interp.c` into an executable named `calc_interp` in the same directory using `gcc`.
   - Run the updated `run_data.py` script using `python3`, passing `data.csv` as the argument.
   - Redirect the standard output of the Python script to a file named `/home/user/pipeline/ci_output.log`.

Do not change the structure of `data.csv` or the intended output format of the Python script. When you have finished, manually execute `./ci_build.sh` so that `ci_output.log` is generated for verification.