You are a data scientist analyzing a mechanical system's ringdown test data. The sensor capturing the vibrations is experiencing a linear drift, and the signal itself is a decaying oscillation with random noise. 

You have been provided a dataset at `/home/user/ringdown_data.csv` containing two columns: `t` (time in seconds) and `y` (measured amplitude).

Your goal is to fit a mathematical model to this data. The theoretical model is:
y(t) = A * exp(-alpha * t) * cos(2 * pi * f * t + phi) + m * t + c

To succeed, you must:
1. Load the data using Python.
2. Use a Fast Fourier Transform (FFT) or spectral analysis to determine the dominant frequency in the signal. You must use this frequency as your initial guess for `f`. If you do not use spectral analysis for the initial guess, your optimization/curve-fitting will likely fail or converge to a local minimum due to numerical instability.
3. Perform a regression/curve-fitting optimization to find the optimal values for the 6 parameters: `A`, `alpha`, `f`, `phi`, `m`, and `c`. Ensure you set appropriate bounds (e.g., `alpha > 0`, `A > 0`) to maintain numerical stability during the optimization.
4. Output your final fitted parameters to a JSON file at `/home/user/fit_results.json`.

The JSON file must have exactly this format:
{
  "A": 0.0,
  "alpha": 0.0,
  "f": 0.0,
  "phi": 0.0,
  "m": 0.0,
  "c": 0.0
}

(Replace 0.0 with your fitted float values).

Assume you have access to standard Python scientific libraries (`numpy`, `scipy`, `pandas`). You may install them if they are missing.