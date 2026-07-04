You are a machine learning engineer preparing a training dataset to predict DNA sequence stability. You are using a Monte Carlo simulation to estimate the expected "binding energy" of sequences under thermal noise. 

You have been provided a script at `/home/user/mc_energy.py` that contains the simulation logic. However, there is a problem: the function `get_expected_energy(seq, num_trials)` produces slightly non-reproducible results even when the random seeds inside the simulation trials are fixed. This is because it uses `multiprocessing.Pool.imap_unordered` and standard floating-point addition `+=`, causing the reduction order of the floating-point results to vary between runs.

Your task is to:
1. Fix `/home/user/mc_energy.py` to guarantee strict reproducibility. You must ensure that the results from the worker pool are collected in a deterministic order (e.g., by using `imap` or `map` instead of `imap_unordered`) AND you must use `math.fsum()` to sum the results before calculating the average to eliminate any floating-point accumulation errors.
2. Write a script `/home/user/generate_data.py` that imports your fixed `get_expected_energy`. 
3. In this script, set `random.seed(42)` and generate 100 random DNA sequences of length 50. (Generate them sequentially using `random.choices("ACGT", k=50)`).
4. For each sequence, calculate its expected energy using `get_expected_energy(seq, num_trials=500)`.
5. Save the results to `/home/user/training_dataset.csv` with two columns: `Sequence` and `Energy`.
6. Use `matplotlib` to plot a histogram of the calculated energies and save it to `/home/user/visualization.png`.

Ensure all files are saved in `/home/user/` and that the CSV values are highly precise and deterministic.