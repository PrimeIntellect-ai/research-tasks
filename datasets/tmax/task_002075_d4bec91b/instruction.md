You are assisting a researcher in extracting chemical kinetic parameters from noisy spectroscopic data. 

We are modeling a reaction system with three species (A, B, and C) described by the following ODE system:
dA/dt = -k1 * A
dB/dt = k1 * A - k2 * B
dC/dt = k2 * B

The provided dataset `/home/user/data/spectroscopy.csv` contains time-series measurements. However, the spectrometer only measures a combined, noisy absorbance signal: `Signal = ε_A * A + ε_B * B + ε_C * C`, where the molar absorptivities are known: ε_A = 2.0, ε_B = 1.0, ε_C = 0.5.

Your goal is to estimate the unknown rate constants (k1, k2) and the initial concentration of species A (A0). We assume B0 = 0 and C0 = 0.

However, our standard non-linear least squares solver is failing with singular matrix inversion errors (or returning wildly unstable results) because the inverse problem is ill-conditioned on this dataset. 

A previous post-doc left a scanned handwritten note containing the Tikhonov regularization parameters needed to stabilize the inversion (a base lambda penalty and specific relative weights for k1, k2, and A0). This image is located at `/app/calibration_note.png`. 

Your tasks:
1. Use any pre-installed CLI tools (like tesseract) to extract the regularization parameters from `/app/calibration_note.png`.
2. Write a Python script to perform a regularized curve fit. You must numerically solve the ODE, compute the Jacobian (e.g., via finite differences or sensitivity equations), and iteratively fit the parameters (k1, k2, A0) to the observed signal.
3. Apply the Tikhonov regularization matrix as described in the calibration note to prevent matrix factorization failures on the near-singular Hessian/Jacobian.
4. Save the final fitted parameters to a JSON file at `/home/user/results/params.json` with the exact keys: `"k1"`, `"k2"`, and `"A0"`.

Ensure your Python script is robust, self-contained, and uses standard scientific libraries (numpy, scipy). The final output must be highly accurate.