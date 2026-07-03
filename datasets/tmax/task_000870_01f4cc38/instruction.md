You are helping a researcher organize and analyze a set of environmental sensor logs. The researcher has a raw dataset located at `/home/user/raw_data.csv` containing four columns: `Timestamp`, `Temperature`, `Humidity`, and `Pressure`.

Your goal is to build a reproducible ETL and analysis pipeline in C++ that processes this data and computes the sample covariance matrix for the three environmental variables (`Temperature`, `Humidity`, and `Pressure`).

Requirements:
1. Write a C++ program at `/home/user/process_data.cpp` that:
   - Reads `/home/user/raw_data.csv`. The first line is a header and should be ignored.
   - Extracts the `Temperature`, `Humidity`, and `Pressure` values as double-precision floating-point numbers.
   - Computes the 3x3 sample covariance matrix for these three variables. (Use the $N-1$ denominator for sample covariance).
   - The ordering of variables in the matrix must be: Temperature (row/col 0), Humidity (row/col 1), Pressure (row/col 2).
   - Writes the resulting 3x3 covariance matrix to `/home/user/covariance.txt`. The format must be exactly three lines, with three space-separated values per line, formatted to exactly 4 decimal places (e.g., using `std::fixed` and `std::setprecision(4)`).

2. Create an executable bash script at `/home/user/run_pipeline.sh` that:
   - Compiles your C++ program using `g++` (e.g., `g++ -O2 process_data.cpp -o process_data`).
   - Executes the compiled program to generate `/home/user/covariance.txt`.

Ensure your C++ code correctly handles standard CSV parsing for this file format and accurately computes the sample covariance.