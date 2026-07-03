You are a performance engineer tasked with profiling a new numerical solver. Your goal is to implement the numerical solver in C++, write a Jupyter notebook to orchestrate benchmarking, and visualize the experimental data.

Complete the following steps:

1. Create a directory `/home/user/perf_test`. All work should be done in this directory.
2. Write a C++ program named `numerical_engine.cpp` that performs numerical integration and differentiation.
   - It must take a single command-line argument `N` (integer), representing the number of sub-intervals.
   - The target function is $f(x) = x^3 - 2x^2 + x$.
   - **Integration:** Compute the definite integral of $f(x)$ from $x = 0$ to $x = 10$ using the Trapezoidal Rule with `N` equal intervals.
   - **Differentiation:** Compute the numerical derivative of $f(x)$ at $x = 5$ using the central difference method, where the step size $h = 10/N$.
   - **Profiling:** Use `<chrono>` to measure the exact execution time of the mathematical computations (integration and differentiation combined) in microseconds. Do not include I/O operations in the timed section.
   - **Output:** The program should print a single line to standard output in the following exact comma-separated format:
     `N,Integral,Derivative,Time_us`
3. Write a Jupyter notebook named `orchestrator.ipynb` (using Python 3) that automates the benchmarking workflow:
   - A cell to compile the C++ program using `g++ -O3 numerical_engine.cpp -o engine`.
   - A cell to run the compiled `engine` for $N \in \{10, 100, 1000, 10000, 100000\}$.
   - A cell to parse the standard outputs and write them to a CSV file at `/home/user/perf_test/results.csv`. The CSV must include a header: `N,Integral,Derivative,Time_us`.
   - A cell to generate a plot of `N` (x-axis, log scale) versus `Time_us` (y-axis) using `matplotlib`, and save the figure as `/home/user/perf_test/timing_plot.png`.
4. Run the notebook headlessly to execute all cells and generate the artifacts. Save the executed notebook as `/home/user/perf_test/orchestrator_executed.ipynb`.
   *(Hint: You can use `jupyter nbconvert --to notebook --execute orchestrator.ipynb --output orchestrator_executed.ipynb`)*

Ensure that after your task is complete, the `results.csv`, `timing_plot.png`, and `orchestrator_executed.ipynb` files exist and contain the correct benchmark data.