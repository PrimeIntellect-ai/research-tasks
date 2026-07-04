You are a performance engineer profiling a data processing application. We have a C++ application that performs linear regression (curve fitting) on a large generated dataset using OpenMP for parallelization. 

The source code is located at `/home/user/regression.cpp`. 

Currently, the program produces slightly different results (slope and intercept) every time it is run. This non-reproducibility is due to the way floating-point reductions are handled across multiple threads. The original developer used `#pragma omp atomic` inside a dynamically scheduled parallel loop, which causes floating-point non-associativity issues due to unpredictable thread execution order.

Your tasks are:
1. Identify and fix the floating-point reduction order issue in `/home/user/regression.cpp` so that the results are strictly reproducible. Replace the `atomic` additions with the proper OpenMP `reduction` clause. Remove the `schedule(dynamic, 1000)` clause and just use the default static schedule.
2. Compile the fixed C++ code into an executable named `/home/user/regression_fixed`. Use `g++` with the `-fopenmp` and `-O2` flags.
3. Run the fixed executable with exactly 4 OpenMP threads (`OMP_NUM_THREADS=4`). 
4. The output of the fixed program should exactly match the reference values provided in `/home/user/reference.txt`. Compare them to ensure your fix is correct.
5. Save the exact standard output of your fixed program (a single line containing `slope,intercept`) to a file named `/home/user/output.txt`.

Ensure all file paths are strictly followed. Do not change the data generation logic or the core regression math formulas, only the OpenMP parallelization directives.