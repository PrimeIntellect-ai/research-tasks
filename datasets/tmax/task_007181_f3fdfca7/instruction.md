You are acting as a data scientist analyzing the decay rate of a chemical concentration over time. You have a single text file at `/home/user/raw_kinetics.txt` containing observational data exported from a legacy sensor. 

The data is stored in a single line with a custom format:
`t=0.0,c=10.00|t=1.0,c=8.19|t=2.0,c=6.70|t=3.0,c=5.49|t=4.0,c=4.49|t=5.0,c=3.68`

We hypothesize that the concentration follows a first-order decay model: 
dc/dt = -k * c

Your task is to estimate the decay constant `k` using the following exact pipeline:
1. Parse the text file to extract the time (`t`) and concentration (`c`) arrays.
2. Compute the numerical derivative (dc/dt) for the *internal* data points (from t=1.0 to t=4.0 inclusive) using the standard central finite difference method: f'(t) ≈ (f(t+h) - f(t-h)) / (2h).
3. Formulate the relationship as an overdetermined linear system `A * k = b`, where `A` is based on the concentration values at the internal points, and `b` is based on the negative derivatives at those same points.
4. Solve for `k` in the least-squares sense using matrix operations (e.g., SVD, QR decomposition, or the normal equations). You may use any language (Python, R, Julia, etc.) and standard linear algebra libraries (like `numpy.linalg`), but do not use high-level regression/curve-fitting wrappers (like `scipy.optimize.curve_fit` or `sklearn.linear_model.LinearRegression`).
5. Save the estimated value of `k` rounded to exactly 3 decimal places to `/home/user/k_estimate.txt`.

Ensure your final output file contains only the numeric value.