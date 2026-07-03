You are an ML Engineer preparing training data for a neural network that predicts the downstream effects of genetic perturbations. To generate this data, you need to simulate the dynamics of several gene regulatory networks using ODEs.

Your task is to write a Python script `/home/user/generate_data.py` that reads a set of network graphs, numerically solves their corresponding ordinary differential equations (ODEs), and outputs the final state of the system to a CSV file.

**Network Graph Format:**
In `/home/user/networks/`, there are several JSON files representing linear gene networks. Each JSON has the following structure:
```json
{
  "nodes": {
    "GeneA": {"init": 100.0, "decay": 0.1},
    "GeneB": {"init": 0.0, "decay": 0.2}
  },
  "edges": [
    {"source": "GeneA", "target": "GeneB", "rate": 0.5}
  ]
}
```

**System Dynamics:**
The concentration $X_i$ of each node $i$ changes over time according to the following linear ODE:
$$ \frac{dX_i}{dt} = -\text{decay}_i \cdot X_i + \sum_{j \to i} \text{rate}_{ji} \cdot X_j $$
Where the sum is over all edges where $j$ is the source and $i$ is the target.

**Requirements for your script:**
1. **Regression Test (Analytical Validation):** Before running the simulations, your script must define and run a function `validate_solver()`. This function should use `scipy.integrate.solve_ivp` (or `odeint`) to simulate a single isolated node with an initial concentration of 100.0 and a decay rate of 0.1 from $t=0$ to $t=50$. It must compare the numerical result at $t=50$ against the exact analytical solution ($100 e^{-5}$). If the absolute difference is less than 0.01, print exactly `"Regression Test Passed"`, otherwise raise an AssertionError.
2. **Graph Parsing & Simulation:** For every `.json` file in `/home/user/networks/`, parse the graph structure, dynamically construct the ODE system, and solve it from $t=0$ to $t=50$.
3. **Data Output:** Extract the final concentration (at $t=50$) for each node in each network. Save the results to `/home/user/training_data.csv`.

**Output Format for `training_data.csv`:**
The CSV must contain a header row: `network_id,node_id,concentration`.
- `network_id` is the filename without the `.json` extension (e.g., `net1`).
- `node_id` is the name of the node.
- `concentration` is the final simulated value, rounded to exactly 4 decimal places.
The rows should be sorted alphabetically by `network_id`, then by `node_id`.

Execute your script to generate the required output.