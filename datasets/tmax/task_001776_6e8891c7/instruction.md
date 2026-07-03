You are a Machine Learning Engineer tasked with setting up a distributed training data generation pipeline for a neural network that detects peaks in Raman spectroscopy data. 

To generate synthetic spectra, your team previously used a high-performance C++ utility. However, the source code was lost, leaving only a compiled, stripped binary located at `/app/spectra_gen`. 

Your goal is to build a Python-based REST API service that wraps this binary, augments the data with realistic noise and baseline drift, analytically validates the generated samples, and serves the data to our ML training workers.

**Task Requirements:**

1. **Understand the Binary (`/app/spectra_gen`)**
   - The binary generates an ideal, noiseless 100-point spectrum (indices 0 to 99). 
   - You need to determine how to pass the 3 parameters of a Gaussian peak: amplitude (`a`), center (`mu`), and standard deviation (`sigma`) via command-line arguments.
   - It outputs the 100 floating-point values to standard output.

2. **Implement the Data API Service**
   - Create a Python web service (using Flask, FastAPI, or similar) listening on `127.0.0.1:8080`.
   - The API must require an authorization header for all endpoints: `Authorization: Bearer ML-DATA-TOKEN`. Returns `401 Unauthorized` if missing or incorrect.
   
3. **Endpoint: `POST /generate`**
   - Accepts a JSON payload: `{"a": float, "mu": float, "sigma": float, "noise_level": float, "baseline_slope": float}`.
   - **Generation:** Execute `/app/spectra_gen` with `a`, `mu`, and `sigma` to get the base 100-point spectrum $S$.
   - **Augmentation:** Add a linear baseline drift to the spectrum such that the value at index $i$ is increased by $i \times \text{baseline\_slope}$ (for $i=0$ to $99$). Then, add Gaussian noise with mean 0 and standard deviation equal to `noise_level`. Let's call this augmented spectrum $S_{aug}$.
   - **Analytical Validation:** To ensure the noise hasn't completely obliterated the peak (which would ruin our training data), you must validate $S_{aug}$. Use `scipy.optimize.curve_fit` to fit the function $f(x) = A \exp(-\frac{(x - M)^2}{2W^2}) + B \cdot x + C$ to the 100 points of $S_{aug}$. 
   - **Response Logic:**
     - If the curve fitting fails to converge, or if the fitted peak center $M$ is more than `2.0` units away from the requested `mu`, the sample is invalid. Return an HTTP `400 Bad Request` with JSON: `{"error": "Validation failed"}`.
     - If validation succeeds, return an HTTP `200 OK` with JSON: `{"spectrum": [list of 100 floats], "fitted_mu": float}` (where `fitted_mu` is the $M$ found by your curve fit).

Start the server as a background process or daemon so it continues running while you finish. Ensure all dependencies (like `scipy`, `numpy`, `flask`/`fastapi`) are installed.