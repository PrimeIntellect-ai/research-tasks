You are an ML Engineer working on an embedded predictive maintenance system. Due to storage constraints, the edge devices log sensor data as raw binary streams. You need to build a high-performance ETL component in C to extract statistical features—specifically, the sample covariance between two sensors—before forwarding the data to the training pipeline.

A raw binary data file is located at `/home/user/sensor_data.bin`. This file contains 1,000 interleaved pairs of IEEE 754 double-precision floating-point numbers (i.e., X1, Y1, X2, Y2, ... X1000, Y1000).

Your task is to:
1. Write a C program at `/home/user/etl_covar.c` that reads the binary file `/home/user/sensor_data.bin` into memory.
2. Use the GNU Scientific Library (GSL) to compute the sample covariance between the X and Y series. You will need to install the appropriate GSL development packages on your system to link against it. The function `gsl_stats_covariance` should be used.
3. The program must write the computed covariance to a text file at `/home/user/covariance_result.txt`, formatted to exactly 6 decimal places (e.g., `1234.567890\n`).
4. Compile your C program to an executable named `/home/user/etl_covar` and run it to generate the result file.

Ensure your program handles errors gracefully (e.g., file not found) and that the final output file contains only the single numeric value.