You are a machine learning engineer preparing clean kinetic training data from raw time-series spectroscopy signals. 

The raw data is located at `/home/user/spectra.csv` (headers: `time,intensity`). 
To generate clean training targets, we need to extract the underlying reaction parameters by fitting the non-linear kinetic model:
`I(t) = A * exp(-k * t) + B`

A colleague wrote a Go program, `/home/user/fit.go`, to fit this model to the data using gradient descent. However, the program is currently failing (producing NaNs). The optimization diverges because the hardcoded step size (learning rate) is poorly adapted to the stiff gradients of the exponential function, much like a numerical integrator diverging due to wrong step-size adaptation.

Your task:
1. Identify the convergence issue in `/home/user/fit.go` and fix it (e.g., implement a smaller learning rate, learning rate decay, or an adaptive step size) so that the gradient descent successfully converges to the true parameters.
2. Run your fixed Go program to find the optimal values for `A`, `k`, and `B` that minimize the Mean Squared Error (MSE).
3. Save the final fitted parameters into a JSON file at `/home/user/params.json` with exactly this structure:
   ```json
   {
     "A": 0.00,
     "k": 0.00,
     "B": 0.00
   }
   ```
   (Round the values to exactly 2 decimal places).

Do not change the objective function (MSE), only fix the optimization process to ensure convergence.