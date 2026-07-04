You are a data scientist preparing to run a gradient descent optimization on a set of models evaluated via Monte Carlo simulations. 

The raw Monte Carlo trial results are stored in a FASTA-like format in `/home/user/mc_results.fasta`. 
In this file, the header lines (starting with `>`) represent the model IDs. The sequence lines contain space-separated numerical values representing the results of individual Monte Carlo trials for that model.

You have noticed that the optimization fails on near-singular inputs—specifically, when a model's Monte Carlo trials show absolute zero variance (i.e., all trial values are exactly identical). This indicates a failure in convergence during the simulation phase.

Your task is to:
1. Parse `/home/user/mc_results.fasta`.
2. Identify models where the trial values are NOT all identical (i.e., filter out the near-singular inputs that failed convergence).
3. For the remaining valid models, calculate the mean of their Monte Carlo trial values.
4. Save the results to `/home/user/valid_models.tsv`.

The output file `/home/user/valid_models.tsv` must be a tab-separated file with two columns:
- Column 1: The model ID (without the `>` character).
- Column 2: The calculated mean, formatted to exactly 3 decimal places.

The final output must be sorted alphabetically by the model ID. Use only standard bash tools (like `awk`, `grep`, `sed`, `sort`, etc.) to complete this task.