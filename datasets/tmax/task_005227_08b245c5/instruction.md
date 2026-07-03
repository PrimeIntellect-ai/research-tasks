You are acting as a bioinformatics analyst. We have a Python script, `/home/user/mutation_sim.py`, which performs a Monte Carlo simulation to estimate the total "mutation burden" across a large dataset of DNA sequences located in `/home/user/sequences.fasta`. 

To speed up the analysis, the script uses `concurrent.futures.ProcessPoolExecutor` to process sequences in parallel. However, our testing framework has flagged a serious issue: running the script multiple times yields slightly different total mutation burdens (at the 12th-15th decimal places) despite the random seeds being strictly tied to the sequence IDs. 

This non-reproducibility is caused by floating-point reduction order differences—the parallel workers complete in a non-deterministic order, and adding their results as they arrive via `as_completed()` changes the intermediate floating-point accumulations.

Your task:
1. Identify the bug in `/home/user/mutation_sim.py` that causes the non-deterministic addition.
2. Modify the script so that the total mutation burden is accumulated strictly in the lexicographical (alphabetical) order of the Sequence IDs, ensuring perfectly reproducible floating-point arithmetic. You must maintain the parallel execution (do not switch to single-threaded).
3. Ensure the script writes the final total burden, formatted to 15 decimal places, to the file `/home/user/reproducible_result.txt`.
4. Run the fixed script to generate this file.

The script relies on `numpy`. You may need to create a python virtual environment in `/home/user/venv`, activate it, and install `numpy` before running the script.