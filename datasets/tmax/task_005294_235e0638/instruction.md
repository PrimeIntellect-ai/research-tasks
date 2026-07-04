You are a data scientist tasked with fitting a network model to sensor data. You have been provided with a time-series dataset of 5 sensors and need to identify which reference model best describes the graph topology of these sensors.

Please write and execute a Python script to perform the following analysis:

1. **Read Data**: Load the time-series data from `/home/user/signals.csv`. This file has 6 columns: `time`, `s1`, `s2`, `s3`, `s4`, and `s5`.
2. **Compute Graph Weights**: Create a $5 \times 5$ weight matrix $W$. The weight $W_{ij}$ between sensor $i$ and sensor $j$ is defined as the definite integral of the absolute difference between their signals over the provided time period:
   $W_{ij} = \int |s_i(t) - s_j(t)| dt$
   Compute this numerical integral using Simpson's rule (`scipy.integrate.simpson`) with respect to the `time` array. Note that $W_{ii} = 0$.
3. **Graph Laplacian**: Construct the Graph Laplacian matrix $L = D - W$, where $D$ is a diagonal degree matrix such that $D_{ii} = \sum_{j} W_{ij}$.
4. **Matrix Decomposition**: Perform Singular Value Decomposition (SVD) on the Laplacian matrix $L$ to extract its singular values. Sort these 5 singular values in ascending order.
5. **Reference Comparison**: Load the reference models from `/home/user/refs.json`. This JSON file maps model names to lists of 5 expected singular values.
6. **Identify Best Fit**: Find the model in the JSON file that minimizes the Euclidean distance (or equivalently, the sum of squared differences) between its expected singular values and your computed, sorted singular values.
7. **Output**: Write the exact string name of the best matching model to `/home/user/best_match.txt`.

Ensure your Python script is executed and the final output file is created successfully.