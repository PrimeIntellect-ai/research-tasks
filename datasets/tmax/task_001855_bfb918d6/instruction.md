You are a Data Scientist tasked with cleaning a massive, noisy dataset of sensor readings. You must build a high-performance C application to parse, analyze, and filter this data efficiently.

**Background:**
A remote sensor array has generated a large binary file located at `/home/user/raw_data.bin`. The file contains contiguous 64-bit IEEE 754 floating-point numbers (`double` in C). No metadata or headers are included.

**Your Objective:**
1. **Analyze:** Write a C program (`/home/user/clean_data.c`) that computes the population mean ($\mu$) and population standard deviation ($\sigma$) of the entire dataset.
2. **Filter (Hypothesis Testing/Bounds):** Identify all "anomalous" sensor readings. An anomaly is defined as any value that falls outside the 3-sigma bounds: $[\mu - 3\sigma, \mu + 3\sigma]$.
3. **Large-Scale Data Storage:** Your C program must use memory-mapped I/O (`mmap`) to read the input file to ensure it can handle datasets larger than available RAM without thrashing. Write the anomalous values (as contiguous `double`s) to a new binary file at `/home/user/anomalies.bin`.
4. **Benchmarking:** Time the execution of the filtering phase (the loop that checks and writes anomalies) using `clock_gettime` or similar high-precision timers. 
5. **Report:** Generate a plain text report at `/home/user/report.txt` with exactly the following format:
   ```
   Mean: <value>
   StdDev: <value>
   Anomalies: <count>
   Time_Seconds: <value>
   ```
   *(Print floating-point numbers to 6 decimal places).*

**Constraints & Execution:**
- You must write, compile, and execute the C code yourself.
- Compile your program to `/home/user/clean_data` using `gcc` with `-O3` optimization.
- Ensure the resulting `/home/user/anomalies.bin` contains only the anomalous 64-bit floats.