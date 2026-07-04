You are a bioinformatics analyst studying the population dynamics of a bacterial wild-type strain and its mutants. You hypothesize that the growth rate $r$ of each sequence is directly proportional to its GC content fraction (the number of 'G' and 'C' bases divided by the total sequence length).

You need to orchestrate a Jupyter Notebook workflow that performs the following steps:
1. Reads a FASTA file located at `/home/user/sequences.fasta`.
2. Computes the GC content fraction for each sequence (e.g., if a sequence is 20 bases long and has 10 Gs and Cs, its $r = 0.5$).
3. Models the population growth of each strain over time using the logistic growth ODE: 
   $$ \frac{dP}{dt} = r \cdot P \left(1 - \frac{P}{K}\right) $$
   where carrying capacity $K = 1000$ and initial population $P(0) = 10$.
4. Solves this ODE from $t = 0$ to $t = 10$ using `scipy.integrate.solve_ivp` (or an analytical solution).
5. Plots the population trajectories $P(t)$ for all sequences on a single graph, clearly labeling each strain. Save this plot to `/home/user/growth_dynamics.png`.
6. Saves the final population sizes at $t = 10$ for each strain to a JSON file at `/home/user/final_populations.json`. The keys should be the sequence IDs (e.g., "WT_strain") and the values should be the population at $t = 10$ rounded to exactly 1 decimal place.

**Execution Requirements:**
You must write your code in a Jupyter Notebook located at `/home/user/workflow.ipynb`. 
Once you have created the notebook, execute it from the command line using `jupyter nbconvert` or `papermill` so that it runs start-to-finish and produces the required output files (`growth_dynamics.png` and `final_populations.json`).

The `sequences.fasta` file is already provided for you in `/home/user/`. Ensure all output files are placed in `/home/user/`.