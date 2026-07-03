You are a performance engineer profiling a complex microservices application. You have intercepted a call trace spanning multiple functions, but the data is raw. You need to reshape this data, model it as a call graph to find the structural bottleneck, and estimate the distribution of its execution times to understand performance jitter.

A raw trace file has been placed at `/home/user/trace.csv`. It contains the following columns: `timestamp`, `caller`, `callee`, `duration`.

Your task is to write and execute a Python script that does the following:
1. Reads `/home/user/trace.csv`.
2. Reshapes the data to construct a directed graph where each node is a function. A directed edge from `caller` to `callee` exists if there is at least one call between them.
3. The weight of each directed edge must be the sum of the `duration` of all calls from that `caller` to that `callee`.
4. Calculates the weighted PageRank for all nodes in the graph using a damping factor (`alpha`) of 0.85. The edge weights must be used in the PageRank calculation.
5. Identifies the "bottleneck" function, which is the node with the highest PageRank score.
6. Extracts all individual `duration` values from the original CSV where the identified bottleneck function was the *callee*.
7. Fits a Gaussian Kernel Density Estimator (KDE) to these specific duration values. Use Scott's rule for the estimator bandwidth (this is the default in `scipy.stats.gaussian_kde`).
8. Calculates the exact mean duration of the calls to the bottleneck function, and evaluates the KDE probability density at this mean value.
9. Writes the results to `/home/user/bottleneck_analysis.txt` in the following exact format:

```text
Bottleneck: <function_name>
Density at mean: <density_value_rounded_to_4_decimals>
```

Constraints and tips:
- Use standard Python libraries such as `networkx`, `pandas`, and `scipy`. You may need to install them.
- Ensure the output text file is created exactly at `/home/user/bottleneck_analysis.txt`.
- Do not include any other text in the output file.