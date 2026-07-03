You are an AI assistant acting as a data scientist analyzing molecular structures. We need to investigate the distribution of atomic displacement parameters (B-factors) in a simulated protein dataset to determine the underlying statistical distribution of the simulation process.

Your task consists of the following steps:

1. **Compile Data Generator**: 
   There is a C source file located at `/home/user/generate_pdb.c`. This program simulates a protein structure and writes standard PDB (Protein Data Bank) format records. Compile this program using `gcc` into an executable named `/home/user/generate_pdb`.

2. **Generate the Data**:
   Run the compiled executable and redirect its output to create a PDB file at `/home/user/simulated.pdb`.

3. **Parse and Analyze**:
   Write a Python script to perform the following analysis:
   - Parse the standard PDB file `/home/user/simulated.pdb` and extract the B-factor values for all `ATOM` records. In standard PDB format, the B-factor is located in columns 61-66 (1-based index) or indices 60:66 in a 0-based string.
   - Fit two different statistical distributions to the extracted B-factor data using maximum likelihood estimation (`scipy.stats`):
     - Normal distribution (`scipy.stats.norm`)
     - Gamma distribution (`scipy.stats.gamma`)
   - Compute the Akaike Information Criterion (AIC) for both fitted distributions to compare the models. 
     The formula for AIC is: `AIC = 2*k - 2*ln(L)`
     where `k` is the number of estimated parameters for the distribution (Normal has 2, Gamma has 3), and `ln(L)` is the log-likelihood of the data given the fitted parameters.
   - Determine which distribution is the best fit (the one with the *lowest* AIC).

4. **Output Results**:
   Your Python script must output the final results into a JSON file at `/home/user/analysis_results.json` with the following exact keys:
   - `"best_fit"`: A string, either `"Normal"` or `"Gamma"`.
   - `"aic_normal"`: A float, the AIC of the Normal distribution (rounded to 2 decimal places).
   - `"aic_gamma"`: A float, the AIC of the Gamma distribution (rounded to 2 decimal places).

Ensure all code runs successfully and the final JSON file is created in `/home/user`. You can install any required Python packages using `pip`.