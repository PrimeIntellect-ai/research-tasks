You are an on-call engineer who just received a 3 AM page. The nightly sensor data aggregation pipeline has failed. 

The pipeline consists of a bash script `/home/user/pipeline/run_all.sh` that compiles and runs a C++ program `/home/user/pipeline/process.cpp` over a set of text files in `/home/user/data/`. 

Recent upstream changes have introduced two new issues:
1. Some data files now have spaces in their filenames, causing the pipeline to break.
2. The sensors have been upgraded to output high-magnitude measurements with small variations (e.g., `100000000.1`, `100000000.2`). The current C++ variance calculation uses a naive formula (`sum_sq/N - (sum/N)^2`) with single-precision floats, leading to catastrophic cancellation (yielding 0 or incorrect values).
3. Occasionally, a sensor will output an invalid text line (e.g., "ERROR" instead of a float). This currently throws an uncaught exception (`std::invalid_argument`) and crashes the C++ program mid-execution.

Your tasks are:
1. **Fix the environment/script:** Modify `/home/user/pipeline/run_all.sh` so it correctly iterates over and processes all files in `/home/user/data/`, including those with spaces in their names.
2. **Fix the crash:** Modify `/home/user/pipeline/process.cpp` to catch parsing exceptions (like `std::invalid_argument` from `std::stod`/`std::stof`) and simply ignore/skip those malformed lines without crashing.
3. **Fix the floating-point precision:** Modify the math logic in `process.cpp` to use double-precision variables (`double`) and implement a numerically stable algorithm for calculating the population variance (e.g., Welford's algorithm, or simply calculating the mean first, then making a second pass to sum the squared differences from the mean). 
4. **Run the pipeline:** Recompile the C++ program (the `run_all.sh` script does this, or you can do it manually with `g++ -O3 /home/user/pipeline/process.cpp -o /home/user/pipeline/process`). Run `run_all.sh`.
5. **Generate the final report:** The fixed C++ program prints `Filename: <basename>, Mean: <mean>, Variance: <variance>`. Ensure the bash script redirects the output of all successful runs to `/home/user/final_report.txt`. Use `std::fixed` and `std::setprecision(4)` for outputting the Mean and Variance.

**Expected Final State:**
A file at `/home/user/final_report.txt` containing the output for all three files in `/home/user/data/`. The script should not crash, and the calculated variances should be mathematically correct despite large baseline numbers.