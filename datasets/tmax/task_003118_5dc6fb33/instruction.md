You are a data scientist working on a pharmacokinetics project. You need to model the concentration of a drug in a two-compartment system (Blood Plasma and Tissue) over time.

You are given a dataset `/home/user/drug_data.csv` containing time-series measurements of the drug concentration in both compartments. The data has columns: `time`, `plasma_conc`, `tissue_conc`.

The system is described by the following system of ordinary differential equations (ODEs):
d(Plasma)/dt = -k1 * Plasma + k2 * Tissue
d(Tissue)/dt = k1 * Plasma - k2 * Tissue

Initial conditions at t=0 are: Plasma = 1.0, Tissue = 0.0.

Your task is to:
1. Write a Python script to numerically solve this ODE and fit the unknown rate constants `k1` and `k2` to the provided data in `/home/user/drug_data.csv` using least squares optimization. Constrain `k1` and `k2` to be positive.
2. Using your fitted `k1` and `k2`, numerically integrate the Plasma concentration from t=0 to t=50 (calculate the Area Under the Curve, AUC, for the plasma compartment).
3. Determine the steady-state probability distribution of the drug between the two compartments. As t -> infinity, the total drug (which remains 1.0) is partitioned between Plasma and Tissue. Let `P = [p_plasma, p_tissue]` be this discrete probability distribution.
4. Calculate the Kullback-Leibler (KL) divergence of your calculated steady-state distribution `P` from a reference target distribution `Q = [0.3, 0.7]` (i.e., compute KL(P || Q)). Use the natural logarithm.

Output your final results into a JSON file located at `/home/user/results.json` with the following exact structure:
```json
{
  "k1": <float>,
  "k2": <float>,
  "auc_plasma": <float>,
  "kl_divergence": <float>
}
```
Ensure your values are accurate to at least 4 decimal places. You may need to install standard scientific Python libraries (like numpy, scipy, pandas) to complete this task.