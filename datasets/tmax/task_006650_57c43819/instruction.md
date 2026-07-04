You are a performance and reliability engineer investigating a statistical anomaly in a newly deployed analytics system. 

The system includes a C++ program located at `/home/user/analytics.cpp` that processes streaming query results. It reads floating-point numbers from standard input (one per line) and calculates the sample variance. Recently, data science teams reported that for datasets with very large mean values but small variances, the system is outputting statistically impossible anomalies (e.g., negative variances or catastrophic precision loss).

Your task:
1. Debug the precision loss occurring in `/home/user/analytics.cpp`. The program currently uses the naive "sum of squares" formula which is highly susceptible to catastrophic cancellation with floating-point numbers.
2. Correct the formula implementation to use a numerically stable method (such as Welford's online algorithm or a stable two-pass approach) to ensure high precision without overflow or cancellation.
3. Compile the corrected program to `/home/user/analytics` using `g++ -O3`.
4. Run the compiled executable against the dataset located at `/home/user/query_results.txt`.
5. Capture the program's standard output (which must be exactly the calculated sample variance printed to 6 decimal places, followed by a newline) and save it to `/home/user/variance_out.txt`.

Ensure your corrected C++ program includes standard headers (`<iostream>`, `<vector>`, `<iomanip>`, etc.) and prints *only* the single numerical value.