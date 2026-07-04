You are an engineer tasked with debugging a long-running data processing service located in `/home/user/sensor_service`. The service consumes high-frequency sensor data, calculates rolling statistics, and is supposed to run indefinitely. However, it currently suffers from three major issues:

1. **Build Failure:** The data preprocessing script (`/home/user/sensor_service/build_data.sh`) fails to execute properly. You need to diagnose and fix the script so it successfully generates `/home/user/sensor_service/sensor_data.csv`.
2. **Memory Leak:** When you run the main service script (`python3 /home/user/sensor_service/processor.py`), it consumes increasing amounts of memory until it crashes. You must identify the root cause of this leak and fix it so the memory footprint remains stable.
3. **Statistical Anomaly (Floating-Point Precision):** The variance calculated by the script is completely wrong (sometimes negative or exactly zero) due to catastrophic cancellation. The sensor values are very large (around 1,000,000) with small variations. You must fix the variance calculation to be numerically stable (e.g., using Welford's algorithm or an appropriate built-in library).

**Your instructions:**
1. Fix `/home/user/sensor_service/build_data.sh` and run it to generate `sensor_data.csv`.
2. Fix the memory leak and floating-point precision issues in `/home/user/sensor_service/processor.py`.
3. Run the fixed `processor.py`.
4. The script should output a file exactly at `/home/user/sensor_service/final_metrics.txt` containing the final calculated variance of the entire dataset in the following format:
`Variance: <value>` (rounded to 4 decimal places).

Ensure the script can process the entire dataset without crashing from memory exhaustion.