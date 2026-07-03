As a bioinformatics analyst, I am working with raw nanopore sequencing signal data. I need to process this 1D electrical current signal, identify the corresponding nucleotide bases by comparing it to a reference model, and perform a statistical hypothesis test to evaluate the fit.

I have two files in `/home/user/`:
1. `reference.csv`: Contains the reference electrical current distributions for four bases. Columns: `base`, `mean_current`, `std_dev`.
2. `signal.csv`: Contains raw signal measurements grouped by events (each event corresponds to a single base). Columns: `event_id`, `current_val`.

Please write and run a Python script to perform the following analysis:

**Step 1: Signal Processing & Base Calling**
For each `event_id` (processed in ascending numerical order):
1. Extract all `current_val` readings for that event.
2. Filter the signal for the event by discarding the single maximum and single minimum values (to remove transient noise spikes). If there are duplicate min/max values, just remove one instance of the min and one instance of the max.
3. Calculate the mean of the remaining values. This is the "observed event mean".
4. Compare the observed event mean to the `mean_current` of each base in `reference.csv`. Assign the base that has the smallest absolute difference between its `mean_current` and the observed event mean.

**Step 2: Sequence Reconstruction**
Concatenate the predicted bases in ascending order of `event_id`, separated by hyphens (e.g., `A-T-C-G`).

**Step 3: Statistical Hypothesis Testing**
To check if our signal perfectly matches the theoretical reference distribution:
1. Create a simulated reference dataset: For each base you predicted in Step 1 (in order), sample exactly 100 points from a Normal distribution using that base's theoretical `mean_current` and `std_dev` from `reference.csv`.
   * *Constraint:* You MUST use `numpy.random.seed(42)` exactly once immediately before starting the sampling loop. Use `numpy.random.normal(loc, scale, 100)` for each predicted base and append the results to a single flat simulated array.
2. Conduct a 2-sample Kolmogorov-Smirnov test (`scipy.stats.ks_2samp`) comparing your list of calculated "observed event means" (from Step 1.3) against the flat simulated reference array.

**Step 4: Output**
Create a file at `/home/user/analysis_result.json` containing exactly these keys:
- `"sequence"`: the reconstructed sequence string.
- `"ks_pvalue"`: the p-value from the KS test, rounded to 4 decimal places.

Ensure the final JSON file is properly formatted.