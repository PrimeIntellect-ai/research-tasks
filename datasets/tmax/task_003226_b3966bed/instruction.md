As a machine learning engineer, you are preparing data for a downstream model by extracting features using Non-negative Matrix Factorization (NMF). 

You have been provided with a basic NMF implementation in `/home/user/mf.py`. However, when you run it on the provided training dataset `/home/user/noisy_data.csv`, the matrix factorization fails and outputs NaNs. This is due to numerical instability caused by near-singular inputs and exact zeros in the data, which leads to division by zero in the multiplicative update rules.

Your task is to:
1. Fix the numerical stability issue in the optimization routine within `/home/user/mf.py`. Specifically, modify the multiplicative update rules for `W` and `H` to add a small epsilon (`1e-9`) to the denominators to prevent division by zero. Do not change the random seed or the initialization logic.
2. Run the modified script to obtain the reconstructed matrix $V_{rec} = W \times H$.
3. Evaluate the quality of the reconstruction by comparing $V_{rec}$ against the clean reference dataset located at `/home/user/reference.csv`. Calculate the Mean Squared Error (MSE) between $V_{rec}$ and the reference matrix.
4. Save the calculated MSE, rounded to exactly 4 decimal places, into a single text file at `/home/user/mse.txt`.

Ensure your final MSE value is correct and your script runs without warnings about division by zero.