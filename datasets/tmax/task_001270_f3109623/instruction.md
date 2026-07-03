You are a Machine Learning Engineer preparing training data and metadata for a structural biology model. You need to build a Bash-based pipeline that orchestrates parsing of bioinformatics files, runs a statistical simulation, and generates a report using a Jupyter Notebook.

Write a bash script at `/home/user/orchestrate.sh` that performs the following steps in order:

1. **FASTA Parsing**: Read the file `/home/user/data/input.fasta`. Count the total number of sequences (indicated by lines starting with `>`). Let this number be $N$.
2. **Monte Carlo Simulation**: Write an inline `awk` or `bash` routine within your script to estimate the value of Pi ($\pi$) using a Monte Carlo method (randomly sampling points in a 1x1 square and checking if they fall within the unit quarter-circle). Use exactly $N \times 10000$ iterations. Save the estimated value of Pi to `/home/user/data/pi_estimate.txt` (just the number).
3. **PDB Parsing**: Read the file `/home/user/data/structure.pdb`. Extract and count the number of `ATOM` records that represent Alpha Carbon atoms. An Alpha Carbon is denoted by the atom name `CA` (typically in columns 13-16 of the PDB ATOM record). Let this count be $C$.
4. **Notebook Orchestration**: Use `papermill` to execute the provided Jupyter notebook `/home/user/templates/report.ipynb`. You must pass $C$ as the parameter `ca_count` and the estimated Pi value as the parameter `pi_estimate`. Save the executed notebook to `/home/user/data/final_report.ipynb`.

Requirements:
- Ensure your script `/home/user/orchestrate.sh` is executable.
- The script should run without interactive prompts and complete successfully.
- All extracted and simulated values must be accurately passed to the notebook.