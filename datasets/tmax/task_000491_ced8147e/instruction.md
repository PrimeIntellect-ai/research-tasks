You are a machine learning engineer preparing a simulated dataset for training a surrogate model. To ensure the dataset is large enough to represent the underlying distribution accurately, you need to perform convergence testing using bootstrap confidence intervals.

You are provided with a data generator source file at `/home/user/generator.cpp`. 

Your task is to:
1. Compile `/home/user/generator.cpp` into an executable named `/home/user/generator` (using `g++ -O3`). This executable takes a single integer argument `N` (the number of samples to generate) and prints `N` floating-point numbers to standard output, one per line.
2. Write a C++ program at `/home/user/bootstrap.cpp` that reads an arbitrary number of `double` values from standard input until EOF. It must then:
   - Compute the 95% bootstrap confidence interval of the sample mean using exactly `B = 1000` resamples.
   - For resampling, use `std::mt19937` initialized with the seed `42`. Use `std::uniform_int_distribution<size_t> dist(0, count - 1)` to pick indices.
   - For each of the 1000 resamples, draw `count` elements (where `count` is the total number of inputs read), compute their mean, and store it.
   - Sort the 1000 bootstrap means in ascending order.
   - The 95% CI is defined by the 2.5th and 97.5th percentiles. Since B=1000, use the element at index `24` as the lower bound and the element at index `974` as the upper bound (0-indexed).
   - Calculate the width of this interval (upper - lower).
   - Print *only* this width to standard output as a standard float/double.
3. Compile `/home/user/bootstrap.cpp` to `/home/user/bootstrap` (using `g++ -O3`).
4. Perform convergence testing by evaluating the CI width for the following sample sizes sequentially: `N = 100, 500, 1000, 5000, 10000`. 
   - Pipe the output of `generator N` into `bootstrap`.
   - Find the **first** (smallest) `N` in that list where the calculated CI width is **strictly less than 0.12**.
5. Once you find this `N`:
   - Run `/home/user/generator N` again and redirect its output to `/home/user/training_data.txt`.
   - Create a log file at `/home/user/convergence_log.txt` containing exactly one line with the successful `N` and its corresponding CI width (separated by a single space, e.g., `5000 0.10432`).

Constraints:
- Do not use external libraries for the bootstrap implementation (only standard C++ library).
- Ensure your bootstrap implementation strictly follows the random generation procedure specified to ensure deterministic verification.