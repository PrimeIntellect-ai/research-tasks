You are an AI assistant helping a computational network researcher. 

I have a set of generated network topologies (representing molecular graphs) and I need to compare their connectivity to a reference dataset. I've written a fast C program to compute the number of connected components using a Union-Find algorithm, but I haven't compiled it or written the analysis pipeline.

Here is what you need to do:
1. Navigate to `/home/user/graph_research/`.
2. Compile the C source code `union_find.c` into an executable named `uf_solver`. Use `gcc` with standard options (e.g., `gcc -O3 union_find.c -o uf_solver`).
3. Write a Python script `/home/user/graph_research/analyze.py` that:
   - Iterates through all 50 text files in the `/home/user/graph_research/graphs/` directory. Each file contains a graph edge list.
   - Executes `./uf_solver <filepath>` for each graph file and captures the stdout, which will be an integer representing the number of connected components.
   - Loads the reference connected component counts from `/home/user/graph_research/reference_data.json` (under the key `"components"`).
   - Performs a Welch's t-test (an independent two-sample t-test with unequal variances) comparing the simulated connected components (from the `graphs/` directory) against the reference components. Use `scipy.stats.ttest_ind` with `equal_var=False`.
4. Run your Python script so that it outputs a JSON file to `/home/user/graph_research/test_results.json` containing exactly these keys:
   - `"t_statistic"`: The calculated t-statistic (float).
   - `"p_value"`: The calculated p-value (float).
   - `"simulated_mean"`: The mean of the connected components calculated from the `graphs/` directory (float).
   - `"reference_mean"`: The mean of the connected components from the reference data (float).

Ensure the `test_results.json` is correctly formatted and contains accurate values based on the graph dataset.