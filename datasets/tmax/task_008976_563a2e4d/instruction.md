You are an IT support technician. We've received Ticket #4092 from the quantitative analysis team. Their historical volatility pricing script is broken and they need it fixed ASAP.

Here is the situation:
The project is located in `/home/user/ticket_4092`.

1. **Dependency Conflict**: The team tried to update their environment, but `requirements.txt` currently has a version conflict preventing installation. Fix `requirements.txt` to install `numpy` and `pandas` successfully in a new virtual environment at `/home/user/ticket_4092/venv`. 
2. **Corrupted Input**: The input file `/home/user/ticket_4092/prices.csv` contains some corrupted rows (e.g., network errors, malformed strings). Modify the script `/home/user/ticket_4092/pricing.py` to gracefully skip any row where the `Price` cannot be parsed as a float, rather than crashing.
3. **System Call Tracing**: The script computes a final "calibrated volatility". The original developer mentioned it reads a multiplier from a hidden configuration file, but forgot to document the file's exact name. If the file is missing, the script silently defaults the multiplier to 0.0, ruining the output. Use system call tracing (e.g., `strace`) to run the script and discover the exact filename it attempts to open in the `/home/user/ticket_4092` directory. Once you find it, create this file and write the value `2.5` into it.
4. **Formula Implementation Correction**: There is a mathematical bug in the `calculate_volatility` function in `pricing.py`. It is supposed to calculate the annualized historical volatility using log returns. The correct formula for a daily log return is $u_i = \ln(P_i / P_{i-1})$. The current script does not compute the natural logarithm, it just calculates the ratio. Fix the mathematical formula in the code.
5. **Regression Test**: Create a regression test script at `/home/user/ticket_4092/test_pricing.py` using the standard `unittest` framework. It must import `calculate_volatility` from `pricing.py` and test it with the exact price list `[100.0, 105.0, 102.9]`. Ensure the test passes.
6. **Final Output**: Run the fixed `pricing.py`. It should process `prices.csv`, calculate the calibrated volatility, and write the successful parsed data and final output to `/home/user/ticket_4092/clean_results.csv` as currently structured in the script.

Your final deliverables that will be automatically checked:
- A working `requirements.txt`
- The properly named hidden configuration file containing `2.5`
- The fixed `pricing.py`
- The passing test suite `test_pricing.py`
- The generated `/home/user/ticket_4092/clean_results.csv`