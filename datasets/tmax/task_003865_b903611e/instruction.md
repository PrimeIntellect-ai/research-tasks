You are a data scientist working on a structural bioinformatics project. We are analyzing the correlation between a protein's local structural flexibility (measured by B-factors) and an array of noisy spectral readings we collected for each residue. 

You need to extract the structural data, reduce the dimensionality of the spectral signals using matrix decomposition, and perform a statistical hypothesis test to determine if adding more spectral components significantly improves our model.

Please perform the following steps:
1. Parse the PDB file located at `/home/user/protein.pdb`. Extract the B-factor (temperature factor) for every `CA` (C-alpha) atom in the order they appear. This will be your target vector, $y$.
2. Load the spectral data from `/home/user/signals.csv`. This file has no headers, and each row corresponds to the `CA` atom at the same index in the PDB file. Let this matrix be $X$.
3. Mean-center the columns of matrix $X$.
4. Perform Singular Value Decomposition (SVD) on the centered matrix to compute the Principal Components (PCs). Use the definition $PCs = U \Sigma$.
5. Fit two Ordinary Least Squares (OLS) linear regression models to predict $y$:
   - **Model 1 (Restricted):** Predict $y$ using only the first Principal Component (PC1) and an intercept term.
   - **Model 2 (Unrestricted):** Predict $y$ using the first three Principal Components (PC1, PC2, PC3) and an intercept term.
6. Conduct an F-test for nested models to compare Model 1 and Model 2. 
7. Create a JSON file at `/home/user/model_comparison.json` containing the F-statistic and the p-value of the test, formatted exactly like this:
```json
{
  "f_stat": 12.3456,
  "p_value": 0.0001
}
```
Round both values to 4 decimal places.