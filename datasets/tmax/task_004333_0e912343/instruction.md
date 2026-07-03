You are tasked with fixing a buggy C extension for Python, managing its dependencies, and using it to perform a schema migration and data backfill on an SQLite database. 

We have a project in `/home/user/project/` that calculates the sum of the first `N` Fibonacci numbers. The core computation is implemented as a C extension for Python to maximize performance. However, the C extension crashes or leaks memory on large inputs due to memory safety issues and undefined behavior.

Here are your objectives:

1. **Package Management**:
   Create a Python virtual environment at `/home/user/venv`. Install any necessary build tools (like `setuptools`) and compile/install the C extension located in `/home/user/project/fib_ext/`.

2. **C/C++ Memory Safety Repair**:
   The C extension source code is at `/home/user/project/fib_ext/fib_ext.c`. It contains two critical bugs:
   - An out-of-bounds array write (buffer overflow) in the Fibonacci generation loop.
   - A memory leak in the Python wrapper function where the allocated C array is never freed before returning the Python list.
   Diagnose and fix both of these issues so the extension is memory-safe and functionally correct. Reinstall the extension in your virtual environment.

3. **Schema Migration and Computation**:
   There is an SQLite database at `/home/user/project/data.db`. 
   It currently contains a single table named `computations` with the schema:
   `CREATE TABLE computations (id INTEGER PRIMARY KEY, n_value INTEGER);`
   
   Write a Python script at `/home/user/project/migrate.py` that:
   - Modifies the schema of the `computations` table to add a new column: `fib_sum INTEGER`.
   - Iterates through all existing rows in the database.
   - For each row's `n_value`, uses the newly fixed C extension (`fib_ext.get_fibs(n)`) to retrieve the list of the first `N` Fibonacci numbers (where `N = n_value`).
   - Calculates the sum of these Fibonacci numbers.
   - Updates the `fib_sum` column for that row with the calculated sum.

4. **Verification Output**:
   At the end of your `migrate.py` script, query the sum of all values in the `fib_sum` column across all rows and write this single integer to `/home/user/project/final_sum.txt`.

Ensure all code runs within the virtual environment and that `/home/user/project/final_sum.txt` contains only the final aggregate sum integer.