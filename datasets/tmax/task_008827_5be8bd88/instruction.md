You are a bioinformatics analyst working with bacterial population growth models. We have a Bash script `/home/user/logistic_euler.sh` that models the logistic growth of different bacterial strains based on their initial sequence-derived parameters. 

The script integrates the logistic growth Ordinary Differential Equation (ODE): `dN/dt = r * N * (1 - N/1000)` from `t=0` to `t=10`. 

However, the script currently uses a hardcoded, overly large step size (`dt=2`), which causes the numerical integrator to diverge and produce nonsensical (or negative) population sizes for fast-growing strains.

Your task:
1. Fix the `/home/user/logistic_euler.sh` script by changing the integration step size `dt` to `0.01`. Ensure the loop boundaries still correctly simulate from `t=0` up to and including `t=10`.
2. A dataset of starting parameters is provided in `/home/user/strains.txt` (Format: `StrainName N0 r`). Run your fixed script for each strain to find the final calculated population (`CalculatedN`).
3. Compare your calculated populations against the gold-standard reference data in `/home/user/reference.txt` (Format: `StrainName ExpectedN`). 
4. Calculate the Mean Absolute Error (MAE) across all strains. The MAE is the average of the absolute differences between `CalculatedN` and `ExpectedN` for each strain.
5. Save the final MAE as a single floating-point number in the file `/home/user/mae.txt`.

Constraints:
- Use standard bash tools (awk, sed, grep, bc, etc.). Do not use Python, R, or other higher-level languages.