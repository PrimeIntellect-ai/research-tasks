You are an AI assistant helping a machine learning engineer prepare training data for a Graph Neural Network (GNN). The model predicts material properties based on localized defect structures in a 2D synthetic crystal. 

Your task is to process a spatial node dataset, perform a domain decomposition around defect centers to extract localized mesh subgraphs, and compute statistical baselines.

**Task Steps:**
1. **Dataset Understanding:** You are provided with two files:
   - `/home/user/nodes.csv`: Contains the `id`, `x`, and `y` coordinates of all atoms in the 2D material.
   - `/home/user/defects.csv`: Contains the `defect_id`, `x`, and `y` coordinates of known defect centers.

2. **Graph Construction & Domain Decomposition:**
   - Construct a global undirected graph where an edge exists between any two nodes in `nodes.csv` if the Euclidean distance between them is strictly less than **$R = 1.5$**.
   - Perform a localized domain decomposition: For each defect in `defects.csv`, extract the induced subgraph containing only the nodes that are within a Euclidean distance strictly less than **$D = 5.0$** from the *defect center's coordinates*.

3. **Feature Extraction:**
   - For each extracted defect subgraph, calculate the **Graph Density**. The density of an undirected graph is $d = \frac{2|E|}{|V|(|V|-1)}$. If a subgraph has fewer than 2 nodes, its density is 0.
   - Collect these density values into an array/list.

4. **Bootstrap Confidence Interval:**
   - We need a robust baseline estimate of the mean defect subgraph density. 
   - Write a Python script to compute the 95% Bootstrap Confidence Interval of the **mean** of these subgraph densities.
   - **Bootstrap specifications:** Use exactly 10,000 resamples (with replacement). Set the random seed to `42` (using `numpy.random.seed(42)` or equivalent) before starting the resampling loop. Use the standard percentile method (2.5th and 97.5th percentiles).

5. **Output Requirement:**
   - Save the final bounds in a JSON file at `/home/user/baseline_ci.json` with the exact keys `"lower_bound"` and `"upper_bound"`.
   - Round the values to exactly 4 decimal places.

*Note: You may install Python libraries like `numpy`, `scipy`, `pandas`, or `networkx` if they are not already available.*