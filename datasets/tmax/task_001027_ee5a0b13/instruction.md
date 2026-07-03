You are an ML engineer preparing a dataset for a model that predicts DNA sequence properties.

You have a Python script located at `/home/user/generate_features.py` that computes three features for a list of DNA sequences provided in `/home/user/sequences.txt`. 

The three features are:
1. **Integration Feature**: The end-point value $y(L)$ of a stability ODE $dy/dt = 100 \cdot (\text{GC\_content}(t) - y)$ with initial condition $y(0) = 0$, integrated from $t=0$ to $t=L$ (where $L$ is the sequence length).
2. **SVD Feature**: The largest singular value of the sequence's one-hot encoded matrix.
3. **Alignment Feature**: The local alignment score between the sequence and a reference primer.

Currently, the script uses a naive fixed-step Euler method for the numerical integration. Because the ODE is stiff, the integration diverges and produces `NaN` or `inf` values for some sequences, causing the script to fail or output useless data.

Your tasks are to:
1. Modify `/home/user/generate_features.py` to fix the numerical integration. Replace the custom Euler method in the `integrate_feature` function with `scipy.integrate.solve_ivp`. Use the `BDF` method (which is suitable for stiff problems) and integrate from $t=0$ to $t=L$.
2. Run the script to process all sequences in `/home/user/sequences.txt`.
3. Ensure the script correctly outputs the features to `/home/user/training_features.csv` with the exact header: `Sequence,Integration,SVD,Alignment`.

Do not change the alignment or SVD logic. The `Integration` column values should be rounded to 4 decimal places in the final CSV.