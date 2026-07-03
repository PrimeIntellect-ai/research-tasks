You are a performance engineer optimizing a bioinformatics pipeline. Your team has a C application that parses a FASTA file and computes a global weighted GC-content metric across thousands of sequences using OpenMP. However, scientists are reporting that the simulation produces non-reproducible results across identical runs due to floating-point reduction order issues.

You need to fix the C code, verify the fix using a Jupyter notebook-based workflow, and perform a statistical hypothesis test to prove the variance has been eliminated.

Here is your environment and task checklist:

1. **Environment Setup:**
   Install any necessary Python packages (like `jupyter`, `notebook`, `scipy`, `pandas`, `numpy`) and C compilers (`gcc`, `libomp-dev`) required for your workflow.

2. **Fix the C Code:**
   The buggy source code is located at `/home/user/score_fasta.c`. It currently uses `#pragma omp atomic` to add floating-point values to a global sum, which causes non-deterministic rounding errors due to unpredictable thread execution order. 
   - Modify `/home/user/score_fasta.c` so that the summation is strictly deterministic (e.g., by writing thread results to an array and doing a sequential sum at the end, or using a deterministic reduction strategy).
   - The compiled program must be executable via: `gcc -O3 -fopenmp /home/user/score_fasta.c -o /home/user/score_fasta`
   - It takes the FASTA file path as its first argument and prints only the final floating-point sum to standard output.

3. **Notebook Orchestration & Statistical Testing:**
   A set of 50 previous, non-deterministic runs is saved in `/home/user/baseline_results.txt` (one float per line).
   Create a Jupyter notebook at `/home/user/evaluate.ipynb` that performs the following regression testing workflow:
   - Programmatically executes your compiled `/home/user/score_fasta` binary 20 times on `/home/user/input.fasta`.
   - Reads `/home/user/baseline_results.txt`.
   - Uses `scipy.stats.levene` to perform Levene's test for equal variances between the baseline results and your new 20 runs.
   - Saves a final JSON report to `/home/user/final_report.json` exactly matching this structure:
     ```json
     {
         "deterministic": true, 
         "p_value": 0.00123,
         "mean_score": 12345.6789
     }
     ```
     (Where `deterministic` is a boolean that is `true` only if all 20 new runs produced the exact same string output, `p_value` is the Levene test p-value, and `mean_score` is the float value of your deterministic runs).

Execute your notebook via the command line (e.g., using `jupyter nbconvert --execute /home/user/evaluate.ipynb` or `papermill`) to generate the `final_report.json`.