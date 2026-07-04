You are a machine learning engineer preparing feature data from a sensor network for a downstream predictive model. 

You have been provided with two files in your home directory:
1. `/home/user/graph.txt`: An edge list of an undirected graph representing the sensor network topology (space-separated, `node_u node_v`).
2. `/home/user/labels.txt`: The target continuous label for each node (space-separated, `node_id label_value`).

Your task is to write a bash script named `/home/user/process_graph.sh` that extracts topological features, fits a statistical distribution, performs curve fitting, and solves a linear equation. The script may utilize standard Linux utilities (like `awk`, `bc`) or call a small inline Python script.

The script must perform the following steps automatically when run:
1. **Graph Algorithm:** Calculate the degree of every node present in `labels.txt` based on the undirected edges in `graph.txt`.
2. **Distribution Fitting:** Calculate the population mean and population standard deviation of these node degrees.
3. **Curve Fitting:** Perform a simple Ordinary Least Squares (OLS) linear regression to predict the label value ($Y$) based on the node degree ($X$). Calculate the slope ($m$) and intercept ($c$).
4. **Equation Solving:** Solve the linear equation $mX + c = 0.5$ to find the "critical degree threshold" ($X$) where the expected label value is exactly $0.5$.

Finally, your script must output these exact five computed values into a JSON file located at `/home/user/results.json`. The JSON file must have the following keys, with values rounded to exactly 4 decimal places:
- `"mean_degree"`
- `"std_degree"`
- `"slope"`
- `"intercept"`
- `"critical_threshold"`

Ensure `/home/user/process_graph.sh` is executable and generates the JSON file correctly when executed.