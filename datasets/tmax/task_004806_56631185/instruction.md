You are a data scientist at a biotech startup analyzing the kinetics of a novel nucleic acid amplification assay. You need to identify a primer sequence from raw sequence data, fit a kinetic growth model to experimental data, and calculate the total expected yield over a specific timeframe via numerical integration.

**Your Tasks:**

1. **Primer Design (Consensus Extraction):**
   - You are provided with a FASTA file at `/home/user/sequences.fasta`. These sequences represent the target region across multiple variant strains.
   - Extract the exact 20-bp consensus sequence starting from the very first position (index 0). Assume no gaps are needed. The consensus should be the most frequent nucleotide at each of the first 20 positions. This will serve as your forward primer.

2. **Kinetic Curve Fitting:**
   - You have experimental fluorescence data in `/home/user/kinetic_data.csv` with columns `time` (in minutes) and `fluorescence`.
   - Fit the data to the logistic growth model: 
     $$F(t) = \frac{K}{1 + \left(\frac{K}{F_0} - 1\right) e^{-r t}}$$
   - Assume $F_0$ is exactly the fluorescence value at time $t=0$ from the CSV.
   - Use non-linear curve fitting to estimate the growth rate ($r$) and the carrying capacity ($K$). Ensure your initial guesses are reasonable (e.g., $r>0$, $K>0$).

3. **Total Yield Estimation (Numerical Integration):**
   - Using your fitted parameters ($r$ and $K$) and the established $F_0$, use numerical integration to calculate the integral of the fitted curve $F(t)$ from $t=0$ to $t=30$ minutes. This represents the cumulative signal yield.

4. **Output Generation:**
   - Create a JSON file at `/home/user/analysis_output.json` containing your final results with the following exact keys:
     - `"primer"`: The 20-bp consensus string (e.g., `"ATGC..."`)
     - `"r"`: The fitted growth rate (rounded to 3 decimal places)
     - `"K"`: The fitted carrying capacity (rounded to 3 decimal places)
     - `"yield_integral"`: The calculated integral from $t=0$ to $t=30$ (rounded to 3 decimal places)

**Environment:**
- You can install any standard Python scientific libraries you need (e.g., `numpy`, `scipy`, `pandas`, `biopython`).
- You must write and execute the Python code to perform this analysis.