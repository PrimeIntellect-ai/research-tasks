You are acting as a performance engineer to fix a critical issue in our spectroscopy processing pipeline. 

We have a C++ application that reads high-frequency spectral intensity data and integrates the signal (calculates the sum). To speed things up, a junior developer recently parallelized the integration using OpenMP. However, we are now seeing non-reproducible results: the final integrated intensity varies slightly across different runs, and it no longer matches our reference dataset's exact value. This is causing downstream pipeline failures. 

The issue is likely due to floating-point reduction order non-determinism combined with precision loss. 

Your task is to:
1. Examine the source code located at `/home/user/spectroscopy_sim.cpp`.
2. Fix the non-reproducibility and precision loss. You should modify the integration logic so that it consistently computes the exact, precise sum of the floating-point values. You must ensure the result is completely reproducible and mathematically accurate (e.g., by using double-precision accumulation and/or deterministic reduction logic like Kahan summation, or simply sequential double-precision summation if you prefer to prioritize accuracy and determinism over the flawed parallel approach).
3. Compile your fixed program using `g++ -O3 -fopenmp /home/user/spectroscopy_sim.cpp -o /home/user/spectroscopy_sim`.
4. Run the program. It reads the dataset from `/home/user/data/spectra.txt`. 
5. The program prints the final integrated value. Save this exact printed value to `/home/user/result.txt`.
6. Create a bash script at `/home/user/verify.sh` that reads the value from `/home/user/result.txt`, reads the expected value from `/home/user/reference.txt`, and compares them. If they match exactly, the script should exit with code 0. Otherwise, it should exit with code 1. Make the script executable.

Ensure that the output of your fixed C++ program is highly consistent and matches `/home/user/reference.txt` perfectly.