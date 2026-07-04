You are an AI assistant helping a computational chemistry researcher run regression tests on a molecular diffusion simulation pipeline. 

The researcher simulates random walks on molecular graph structures to compute steady-state visitation probabilities (a model for molecular diffusion). The simulation is packaged as a parameterizable Jupyter notebook. The researcher needs a Bash-based regression testing harness to execute the notebook, calculate the distance between the output probability distribution and a known baseline, and determine if the simulation passes.

Your task is to orchestrate this workflow by writing a Bash script.

**Prerequisites:**
You will need to install the following Python packages (using `pip`):
- `papermill` (for notebook orchestration)
- `jupyter`
- `networkx`
- `pandas`

**Initial Workspace Context:**
The researcher has prepared a workspace at `/home/user/sim_project` with the following files:
- `/home/user/sim_project/lattice.edgelist`: A space-separated edgelist of the molecular graph.
- `/home/user/sim_project/diffusion.ipynb`: The simulation notebook. It expects two string parameters: `graph_path` (path to the edgelist) and `output_path` (path to save the resulting CSV).
- `/home/user/sim_project/ref_dist.csv`: The baseline probability distribution. It has a header `node,prob` and contains the reference steady-state probabilities for each node.

**Task Requirements:**
Write a Bash script at `/home/user/run_regression.sh` that performs the following steps:

1. **Notebook Orchestration**: 
   Use `papermill` to execute `/home/user/sim_project/diffusion.ipynb`. 
   Pass the parameters:
   - `graph_path` = `/home/user/sim_project/lattice.edgelist`
   - `output_path` = `/home/user/sim_project/test_dist.csv`
   Save the executed notebook output to `/home/user/sim_project/diffusion_executed.ipynb`.

2. **Probability Distribution Distance**: 
   The simulation will produce `/home/user/sim_project/test_dist.csv` with the header `node,prob`.
   Using strictly Bash commands and standard POSIX utilities (like `awk`, `join`, `sort`), compute the **Total Variation Distance (TVD)** between the distributions in `test_dist.csv` and `ref_dist.csv`. 
   *Note: Total Variation Distance between two discrete probability distributions P and Q is defined as exactly half the L1 distance: TVD = 0.5 * sum(|P(x) - Q(x)|) for all x.*

3. **Logging & Evaluation**:
   Write the calculated TVD exactly to `/home/user/regression_result.log` in the following format:
   `TVD=<calculated_value>`
   (Format the value to 4 decimal places).
   
   If the TVD is strictly less than `0.05`, the script should print `PASS` to standard output and exit with status code `0`.
   If the TVD is `0.05` or greater, print `FAIL` to standard output and exit with status code `1`.

Make sure `/home/user/run_regression.sh` is executable and run it once to generate the final log file and executed notebook.