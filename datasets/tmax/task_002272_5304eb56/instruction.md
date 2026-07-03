You are a machine learning engineer preparing training data for a Graph Neural Network that predicts chemical reaction dynamics. 

You need to simulate a simple consecutive reaction network (A -> B -> C), compare it with an existing set of experimental reference data, extract graph features, and visualize the results.

The experimental reference data is provided in a CSV file at `/home/user/exp_data.csv`. It contains columns `time`, `A`, `B`, and `C`.

Your tasks are:
1. **ODE Simulation**: Numerically solve the ODE system for the reaction network A -> B -> C.
   - The rate equations are: 
     - dA/dt = -k1 * A
     - dB/dt = k1 * A - k2 * B
     - dC/dt = k2 * B
   - Parameters: `k1 = 0.5`, `k2 = 0.2`.
   - Initial conditions: A(0) = 100, B(0) = 0, C(0) = 0.
   - You must evaluate your ODE solution at the exact time points specified in the `time` column of `/home/user/exp_data.csv`.

2. **Reference Comparison**: Calculate the Mean Squared Error (MSE) between your ODE simulation and the experimental data for species A, B, and C independently.

3. **Graph Features**: Treat the reaction network as a directed graph where chemical species are nodes and the reactions are directed edges (an edge from A to B, and an edge from B to C). Determine the in-degree and out-degree of each node.

4. **Data Aggregation**: Save a JSON file at `/home/user/training_entry.json` containing the calculated metrics. The JSON must exactly follow this schema:
   ```json
   {
     "mse_A": <float>,
     "mse_B": <float>,
     "mse_C": <float>,
     "max_B_simulated": <float>, 
     "graph_features": {
       "A": {"in": <int>, "out": <int>},
       "B": {"in": <int>, "out": <int>},
       "C": {"in": <int>, "out": <int>}
     }
   }
   ```
   *Note: `max_B_simulated` should be the maximum concentration of B found across the evaluated time points in your ODE solution.*

5. **Visualization**: Create a line plot visualizing both the simulated data (as solid lines) and the experimental data (as scattered points) for A, B, and C over time. Save this plot to `/home/user/kinetics_plot.png`.

You may use Python or any other language/tools of your choice. If you use Python, you might need to install packages like `scipy`, `pandas`, `numpy`, and `matplotlib` via pip.