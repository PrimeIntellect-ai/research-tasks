You are a data scientist analyzing spectral data for a chemical mixture. You need to determine the concentration of four reference compounds in a mixture spectrum. However, two of the compounds have highly overlapping spectra, making the reference matrix near-singular and causing standard ordinary least squares (OLS) to fail or produce wildly unstable results.

Your task is to write a Python script at `/home/user/analyze_mixture.py` that processes the data, performs a robust matrix decomposition, and compares the results against historical bounds.

Here are the requirements:

1. **Environment Setup:** 
   Install any necessary Python libraries (e.g., `numpy`, `pandas`, `scipy`) in your user environment.

2. **Data Processing:**
   - Read the reference spectra from `/home/user/spectroscopy/refs.csv`. This file has columns: `Wavelength`, `Comp1`, `Comp2`, `Comp3`, `Comp4`.
   - Read the mixture spectrum from `/home/user/spectroscopy/mixture.csv`. This file has columns: `Wavelength`, `Intensity`.
   - **Baseline Correction:** The mixture spectrum has a background baseline artifact. Fit a 2nd-degree polynomial ($ax^2 + bx + c$) to the `Wavelength` vs `Intensity` data of the mixture. Subtract this fitted polynomial baseline from the `Intensity` to get the `Corrected_Intensity`. Do *not* baseline-correct the reference spectra.

3. **Matrix Factorization (Robust Regression):**
   - Let $X$ be the design matrix consisting of the 4 reference spectra columns (in order: Comp1, Comp2, Comp3, Comp4), and $y$ be the `Corrected_Intensity`.
   - To handle the near-singularity of $X$, compute the Moore-Penrose pseudoinverse using Singular Value Decomposition (SVD). 
   - **Crucial Step:** When computing the pseudoinverse $X^+$, explicitly truncate (discard/set to zero inverted singular values) any singular values of $X$ that are strictly less than `0.05`. 
   - Compute the concentration coefficients $\beta = X^+ y$.

4. **Reference Comparison & Reporting:**
   - Read `/home/user/spectroscopy/historical_bounds.json`, which contains min and max acceptable concentrations for each component.
   - Generate a report file at `/home/user/spectroscopy/report.txt`.
   - The first line must list the four original (untruncated) singular values of $X$ in descending order, formatted to exactly 4 decimal places, separated by commas.
   - The next four lines must list the computed concentration for each component (formatted to 4 decimal places) and whether it is `IN_BOUNDS` or `OUT_OF_BOUNDS` according to the JSON file (inclusive of the bounds).

**Output Format for `/home/user/spectroscopy/report.txt`:**
```
Singular values: s1, s2, s3, s4
Comp1: [value] (STATUS)
Comp2: [value] (STATUS)
Comp3: [value] (STATUS)
Comp4: [value] (STATUS)
```
*(Replace `s1...s4`, `[value]`, and `STATUS` with your computed numbers and evaluations.)*