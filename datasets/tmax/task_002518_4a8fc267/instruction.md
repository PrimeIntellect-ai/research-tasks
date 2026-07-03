You are a performance engineer tasked with optimizing a scientific computing application. 

We have a C++ Monte Carlo energy calculation program located at `/home/user/mc_sim.cpp`. It uses a multi-dimensional array to compute the energy states of a system. However, the application is running significantly slower than expected. 

Your analysis suspects that the `calculate_energy` function is suffering from severe cache thrashing due to an incorrect array traversal pattern (accessing data in a non-cache-friendly order).

Your tasks are:
1. Inspect `/home/user/mc_sim.cpp` and fix the multi-dimensional array manipulation in the `calculate_energy` function so that it traverses the 2D `std::vector` in a cache-friendly, row-major order (standard for C++).
2. Compile the fixed program using `g++ -O3 -o /home/user/mc_sim /home/user/mc_sim.cpp`.
3. Run the compiled executable.
4. Save the exact numerical output of the program into a log file at `/home/user/report.txt`.

Ensure the loop logic is unchanged other than the traversal order (do not hardcode the expected output; the compilation and execution must work properly).