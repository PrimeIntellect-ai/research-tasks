You have inherited an unfamiliar Python codebase responsible for processing critical sensor data. The main script is located at `/home/user/sensor_aggregator.py`.

Currently, the script is broken. When executed, it exits with a non-zero status code and produces no output. Your goal is to debug, repair, and successfully run this script so that it produces the correct aggregated output.

Here is what you need to know:
1. The script reads input data from `/home/user/sensor_data.txt`.
2. The script is expected to write its final calculated result to `/home/user/output.txt`.
3. The previous developer mentioned that the script uses chunk-based processing, but they noticed some "unexpected crashes with edge-case data sizes" before they left. 
4. The calculation is highly sensitive. The data stream contains extreme fluctuations (massive spikes and drops alongside minor baseline readings). You must ensure that the final aggregation does not suffer from precision loss.

Your tasks:
1. Diagnose and fix the silent failure preventing the script from even starting its processing. (Hint: trace the system calls if you can't figure out why it's exiting).
2. Fix the chunking logic so that the script successfully processes all the input data without crashing on edge cases.
3. Fix the aggregation logic to accurately preserve floating-point precision across extreme value fluctuations.
4. Run the fixed script so that the correct sum is written to `/home/user/output.txt`.

Do not change the input data file `/home/user/sensor_data.txt`. Only modify `/home/user/sensor_aggregator.py` and your environment as needed.