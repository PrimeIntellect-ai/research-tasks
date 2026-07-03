You have just inherited a legacy sensor monitoring application. The system reads streaming telemetry data and calculates rolling statistical metrics (mean and standard deviation) to detect anomalies. 

However, the application is crashing intermittently with a `ValueError: math domain error`. The previous developer left behind the codebase and a sample data file that reliably triggers the crash.

Your objectives:
1. **Investigate the anomaly**: Run the existing processing script against the provided data to reproduce the crash. 
2. **Create a Minimal Reproducible Example (MRE)**: Create a script at `/home/user/mre.py` that isolates the bug. It must instantiate the stats class, feed it *only* the specific minimal sequence of numbers that causes the crash (based on the system's state right before the failure), and catch/print the resulting exception.
3. **Correct the formula**: The variance calculation in `/home/user/stats.py` suffers from catastrophic cancellation (floating-point precision loss). Fix the implementation in `/home/user/stats.py` so that it is numerically stable (e.g., using Welford's algorithm or correctly bounding the variance) and does not crash.
4. **Verify the fix**: Run the fixed application over the entire dataset and redirect the successful output to `/home/user/success.txt`.

**Files provided (already in your environment):**
- `/home/user/stats.py`: Contains the `StreamingStats` class.
- `/home/user/process.py`: The main entry point that reads data and uses `StreamingStats`.
- `/home/user/sensor_data.csv`: The dataset causing the failure.

**Success Criteria:**
- `/home/user/mre.py` exists, uses a hardcoded minimal list of floats, and demonstrates the crash.
- `/home/user/stats.py` is fixed and handles the statistical calculations without raising domain errors on valid sensor data.
- `/home/user/success.txt` exists and contains the complete, successful output of `python3 /home/user/process.py`.