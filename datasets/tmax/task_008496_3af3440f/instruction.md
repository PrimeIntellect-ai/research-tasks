You are a performance engineer profiling a new message-routing application for molecular networks. The application processes various network topologies, and you need to establish the expected baseline "routing cost" (shortest path distance) across a batch of sample networks, including a statistically sound confidence interval.

You have been provided a dataset of molecular network graphs in `/home/user/network_data.txt`. 

Your task is to write a C++ program (`/home/user/profile.cpp`) and a Python visualization script (`/home/user/plot.py`) to perform this analysis.

Step 1: Graph Algorithm (C++)
Write a C++ program that reads `/home/user/network_data.txt`.
The file format is:
- The first line contains an integer `N` (the number of graphs).
- This is followed by `N` blocks describing each graph.
- Each block starts with two integers `V` (number of vertices) and `E` (number of edges).
- The next `E` lines contain three integers `u v w`, representing an undirected edge between node `u` and node `v` with weight `w`.
For each graph, calculate the shortest path distance from node `0` to node `V-1` using Dijkstra's algorithm. If node `V-1` is unreachable, consider the distance to be `0` (for this specific profiling scenario). Store these `N` distances in an array in the order the graphs appear.

Step 2: Bootstrap Confidence Interval (C++)
In the same C++ program, implement a bootstrap resampling procedure to calculate the 95% confidence interval for the mean of these `N` distances.
- Perform exactly `10000` bootstrap iterations.
- In each iteration, draw `N` samples with replacement from your calculated distances.
- Calculate the mean of these `N` samples (as a `double`).
- Save the 10,000 means to a file named `/home/user/bootstrap_means.txt` (one mean per line, in the order they were generated).
- To ensure reproducibility for our automated tests, you MUST use `std::mt19937` initialized with a seed of `42`. For drawing samples, use `std::uniform_int_distribution<int> dist(0, N - 1)`. Draw the `N` indices for iteration 0, then the `N` indices for iteration 1, and so on.
- After generating the 10,000 means, sort them in ascending order.
- Determine the 95% confidence interval using the percentile method: the lower bound is the value at index 250 (the 2.5th percentile), and the upper bound is the value at index 9750 (the 97.5th percentile), assuming 0-based indexing.
- Write the lower and upper bounds to `/home/user/ci_result.txt` in the exact format: `Lower: <value>, Upper: <value>` (formatted to 2 decimal places).

Step 3: Visualization (Python)
Write a Python script `/home/user/plot.py` that reads `/home/user/bootstrap_means.txt` and generates a histogram of the bootstrap distribution.
- Use `matplotlib.pyplot`.
- Create a histogram with 50 bins.
- Add a vertical red dashed line for the lower bound and another for the upper bound.
- Set the title to "Bootstrap Distribution of Mean Routing Costs".
- Save the plot as `/home/user/distribution.png`.

Compile your C++ code with standard optimization (`g++ -O2 profile.cpp -o profile`), run it, and then run your Python script.