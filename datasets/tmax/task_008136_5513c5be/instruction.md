I am a data scientist working with a large batch of sensor telemetry. Our edge devices have uploaded a "wide format" dataset to a remote staging directory, and I need you to build a high-performance C program to process it.

Here is what you need to do:

1. **Transfer Data**: Copy the raw dataset from the staging directory at `/tmp/remote_data/sensor_readings.csv` to your working directory `/home/user/workspace/`.
2. **Transform & Calculate**: Write a C program (`/home/user/workspace/process.c`) that:
   - Reads the CSV file. The file has a header: `DeviceID,T0,T1,T2,T3,T4,T5,T6,T7,T8,T9`. Each subsequent row contains an integer DeviceID followed by 10 floating-point sensor readings corresponding to those time steps.
   - Reshapes this wide-format data into a logical "long format" (DeviceID, TimeStep, Value) in memory.
   - Groups the data by `TimeStep` (T0 through T9) and calculates the **Sum of Squares** of the values for each time step across all devices.
   - **Parallelization**: You must use OpenMP or pthreads in your C program to process the data or calculate the sums in parallel.
3. **Output**: Your C program must write the final aggregated results to `/home/user/workspace/metrics.csv`.
   - The output CSV must have the header `TimeStep,SumOfSquares`.
   - Each row should list the time step (e.g., `T0`) and the sum of squares formatted to exactly two decimal places (e.g., `T0,12345.67`).
   - The output must be sorted by the TimeStep in ascending order (T0 to T9).

Compile your C program, run it, and ensure `metrics.csv` is generated correctly.