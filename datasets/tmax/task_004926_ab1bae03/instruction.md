You are tasked with building a hybrid Python/C data processing utility. You have been provided with a C source file at `/home/user/math_lib.c` which contains a numerical algorithm to calculate the population variance of an array of floats. A SQLite database also exists at `/home/user/data.db` containing a table `records` with columns `id INTEGER PRIMARY KEY` and `input_mean REAL`.

Perform the following tasks:

1. **Polyglot Build:** Compile `/home/user/math_lib.c` into a shared library at `/home/user/libmath.so`.
2. **Schema Migration:** Safely migrate the SQLite database at `/home/user/data.db` by adding a new column to the `records` table named `variance` of type `REAL`.
3. **Data Processing Script:** Write a Python script at `/home/user/process.py` that accepts a single command-line argument `--data` followed by a comma-separated string of numbers.
   - **Request Validation:** The script must validate that the input consists of *exactly* 5 integers, and that each integer is between 0 and 100 inclusive. If the input is invalid, the script must write the exact string `INVALID_INPUT` to `/home/user/error.log` and exit gracefully.
   - **Numerical Execution:** If the input is valid, calculate the mean of the 5 integers in Python. Then, use the `ctypes` module to pass the 5 integers (as floats) to the `calc_variance(float* arr, int n)` function in `/home/user/libmath.so` to compute their variance.
   - **Data Persistence:** Insert a new row into the `records` table in `/home/user/data.db` containing the computed `input_mean` and `variance`.
4. **Execution:** After creating the script, test it by running:
   `python3 /home/user/process.py --data "10,20,30,40,50"`
   and then test the validation by running:
   `python3 /home/user/process.py --data "150,20"`

Ensure your final database has the new schema and the inserted row, and that the error log contains the validation failure.