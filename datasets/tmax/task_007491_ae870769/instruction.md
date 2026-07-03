You are a performance engineer profiling a scientific application. You have two files in your home directory: `/home/user/spectro.cpp` (a C++ application that performs mesh refinement and spectroscopy signal processing) and `/home/user/density.py` (a Python script that performs density estimation on the output).

Your task is to create a reproducible pipeline shell script at `/home/user/pipeline.sh` that does the following:
1. Compiles `/home/user/spectro.cpp` into an executable named `spectro` using `g++` with optimizations (`-O2`) and GNU profiler flags enabled (`-pg`).
2. Runs the `spectro` executable. This will generate a file named `peaks.csv` and a profiling data file `gmon.out`.
3. Analyzes the profiling data using `gprof`. Extract the `% time` (the first column of the flat profile) spent specifically in the `refine_mesh()` function. Write *only* this numeric value to `/home/user/metrics.txt`.
4. Runs `/home/user/density.py`, which reads `peaks.csv`, fits a Gaussian Kernel Density Estimate (KDE) to the spectroscopy peaks, and prints the maximum density value. Append this printed value as a new line to `/home/user/metrics.txt`.

Ensure your `/home/user/pipeline.sh` script is executable and runs successfully. 
Do not modify `spectro.cpp` or `density.py`.