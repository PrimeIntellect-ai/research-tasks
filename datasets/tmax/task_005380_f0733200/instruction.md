You are an ML Engineer preparing training data. You need to verify that your validation dataset is drawn from the same distribution as your training dataset for a specific critical feature. To do this, you will implement a reproducible computation pipeline that calculates a probability distribution distance metric: the two-sample Kolmogorov-Smirnov (KS) statistic.

Your task is to write a C++ program and a bash wrapper script to perform this statistical hypothesis comparison.

1. Two input files already exist on your system:
   - `/home/user/train_data.txt`
   - `/home/user/val_data.txt`
   Each file contains a single column of floating-point numbers (one per line).

2. Write a C++ program at `/home/user/compute_shift.cpp` that takes exactly two file paths as command-line arguments (Train data, then Val data).
   - The program must read the numbers from both files.
   - It must compute the empirical Cumulative Distribution Function (eCDF) for both datasets.
   - It must calculate the two-sample KS distance, which is the maximum absolute difference between the two eCDFs across all data points: `D = sup_x |F_{train}(x) - F_{val}(x)|`.
   - The program should output exactly two lines to standard output:
     - Line 1: The KS distance, formatted to exactly 4 decimal places (e.g., `0.1425`).
     - Line 2: The result of the hypothesis test. Print `REJECT` if the KS distance is strictly greater than `0.05` (meaning the distribution shift is too large), otherwise print `ACCEPT`.

3. Write a bash script at `/home/user/run_pipeline.sh` that ensures this is a reproducible pipeline. The script must:
   - Compile the C++ program using `g++ -O3 -std=c++17 /home/user/compute_shift.cpp -o /home/user/compute_shift`.
   - Execute the compiled program passing `/home/user/train_data.txt` and `/home/user/val_data.txt` as arguments.
   - Redirect the standard output of the program to `/home/user/shift_report.txt`.

Ensure your bash script is executable. Run your bash script so that `/home/user/shift_report.txt` is generated.