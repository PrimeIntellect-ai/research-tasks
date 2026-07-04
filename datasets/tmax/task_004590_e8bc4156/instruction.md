You are a performance engineer working on a computational biology project. Our team has a C++ application, `spectral_analyzer`, which performs a basic sequence alignment of spectral peaks and then uses a nonlinear solver to determine an optimal calibration coefficient. 

Recently, the application has been failing on a new high-resolution reference dataset due to numerical instability. The tool uses a naive variance calculation for the spectral alignment scores, which suffers from catastrophic cancellation when the values are large and very close to each other. This results in negative variances being passed to the nonlinear equation solver, which then produces `NaN` results.

Your task is to:
1. Review the source code located at `/home/user/project/spectral_analyzer.cpp`.
2. Identify the function `calculate_variance` and replace the naive one-pass variance algorithm ($E[X^2] - E[X]^2$) with a numerically stable algorithm (such as a two-pass mean/variance calculation or Welford's online algorithm).
3. Compile the code using `g++ -O3 -std=c++11 -o spectral_analyzer spectral_analyzer.cpp`.
4. Run the newly compiled application on the reference dataset located at `/home/user/project/dataset.txt`.
5. The program takes a single file argument: `./spectral_analyzer /home/user/project/dataset.txt`.
6. Pipe the standard output of the fixed program to `/home/user/project/results.log`.

The output written to `/home/user/project/results.log` must precisely match the format:
```
Mean: <value>
Variance: <value>
Calibration Coefficient: <value>
```
Values should be printed to 4 decimal places.

Ensure you complete all the above steps. Do not use external libraries beyond the C++ standard library.