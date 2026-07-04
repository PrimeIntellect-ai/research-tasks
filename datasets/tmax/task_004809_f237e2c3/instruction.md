You are helping me debug a failing build process for a data-aggregation utility. 

I have a Bash script located at `/home/user/project/build_model.sh` that processes sensor readings from `/home/user/project/sensor_data.txt` to calculate a converged baseline value. 

However, the script is currently failing for a few reasons:
1. **Corrupted Input:** The sensor data file contains occasional corrupted, non-numeric lines (e.g., `ERR_TIMEOUT`). The script currently tries to process these, which breaks the arithmetic operations.
2. **Convergence Failure & Precision Loss:** The script iteratively refines a `BASELINE` variable. It calculates the average of the inputs and then applies an update formula: `BASELINE = (BASELINE + AVERAGE) / 2`. It stops when the difference between the old and new baseline is strictly less than `0.01`. However, because the original author used Bash's native `$(( ... ))` arithmetic, precision is lost (integer truncation occurs), and the script oscillates or converges to the wrong integer value, often failing the build checks.

Your tasks:
1. **Fix the corrupted input handling**: Modify `/home/user/project/build_model.sh` so it completely ignores any lines in `sensor_data.txt` that are not valid integers or floats.
2. **Fix the precision loss**: Replace the Bash integer arithmetic with a tool that handles floating-point math accurately (like `awk` or `bc -l`). Ensure all math retains at least 4 decimal places of precision during calculation.
3. **Trace the intermediate states**: Before the script exits, it must write a trace log of every iteration's updated `BASELINE` value to `/home/user/project/trace.log`. The format should be exactly `Iteration X: YYYYY` (e.g., `Iteration 1: 10.0000`), with the value printed to 4 decimal places.
4. **Output the final result**: The script should output ONLY the final converged baseline value to `/home/user/project/final_output.txt` (formatted to exactly 4 decimal places).

Run the script to ensure your fixes work. Do not change the overall logic of the convergence loop, just fix the input parsing, the math precision, and add the required file outputs.