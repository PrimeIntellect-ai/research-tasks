You have inherited an unfamiliar codebase for a sensor telemetry processor. The previous developer left abruptly, and the main data processing pipeline is crashing.

You will find the project repository at `/home/user/sensor_project`. 
Inside, there are three files:
1. `sensor_data.txt`: A dataset of high-precision floating-point sensor readings.
2. `processor.c`: A C program designed to calculate a moving average (window size 5) and a running sample variance.
3. `run_pipeline.sh`: A shell script that compiles the program and runs it on the data.

Currently, if you run `./run_pipeline.sh`, the C program crashes with an assertion failure before completing. The crash logs are visible in the terminal output.

Your objectives:
1. Diagnose the assertion failure using the error messages. The failure is caused by **numerical instability** (catastrophic cancellation) in the variance formula, which uses single-precision floats and the naive variance algorithm. Fix the C code by implementing Welford's online algorithm using `double` precision to guarantee stability.
2. There is a second bug: an **off-by-one boundary condition** in the moving average window calculation that occasionally includes garbage memory, skewing the moving average. Identify and fix this logical error.
3. Once the code is stable and logically correct, compile `processor.c` (e.g., `gcc -O2 processor.c -o processor -lm`) and run it on `sensor_data.txt`.
4. Save the standard output of the corrected program to `/home/user/sensor_project/processed_output.csv`.

Format constraints for `processed_output.csv`:
- The output must include the header: `Line,Value,MovingAvg,RunningVar`
- Followed by the correctly calculated values for each line in `sensor_data.txt`, comma-separated.
- `Value` and `MovingAvg` should be printed to 2 decimal places (`%.2f`).
- `RunningVar` should be printed to 6 decimal places (`%.6f`).

Do not change the window size (it must remain 5). The running variance is computed over *all* data seen up to that point, not just the window.