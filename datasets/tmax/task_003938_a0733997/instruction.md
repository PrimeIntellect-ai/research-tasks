You are a DevOps engineer responsible for maintaining a data processing pipeline. Our nightly log aggregation job is intermittently failing. 

The pipeline processes numerical sensor logs using a custom C++ utility. The runner script `/home/user/run_pipeline.sh` feeds all `.csv` files in `/home/user/logs/` to the C++ binary `/home/user/bin/sensor_aggregator`.

Recently, the job started crashing on certain log batches with a `std::runtime_error` related to a mathematical domain error, stopping the entire pipeline. 

Your tasks are to:
1. Reproduce the error to identify which log file is causing the crash.
2. Debug and fix the numerical instability in the C++ source code located at `/home/user/src/sensor_aggregator.cpp`. The program calculates the mean and standard deviation of sensor readings. The current implementation suffers from catastrophic cancellation (floating-point precision loss) when processing values that are large but very close to each other.
3. Modify the code to use a numerically stable method for calculating the variance/standard deviation (e.g., calculating the mean first, then the sum of squared differences, or using Welford's algorithm).
4. Recompile the fixed binary to `/home/user/bin/sensor_aggregator` (use `g++ -O2 /home/user/src/sensor_aggregator.cpp -o /home/user/bin/sensor_aggregator`).
5. Run the pipeline script again and save the successful output to `/home/user/pipeline_success.out`.

Ensure `/home/user/pipeline_success.out` contains the processed output of all log files without any crashes. Do not alter the output formatting of the C++ program, only fix the mathematical calculation.