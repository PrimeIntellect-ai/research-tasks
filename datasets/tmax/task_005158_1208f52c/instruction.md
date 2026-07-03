You are a data scientist analyzing messy spectroscopy data. Your goal is to extract the signal peak area from a specific sensor's readings while modeling and subtracting a background baseline.

You must orchestrate your entire workflow in a Jupyter Notebook and execute it. 

Here are the requirements:
1. **Data Reshaping:** Read the dataset located at `/home/user/spectroscopy_data.csv`. Filter the dataset to retain only the rows where `sensor_id` is `"A1"`. Sort the remaining rows by `wavelength` in ascending order.
2. **Signal Processing:** The `intensity` data contains high-frequency noise. Apply a Savitzky-Golay filter to the `intensity` column using a window length of 5 and a polynomial order of 2. Use `scipy.signal.savgol_filter` with its default padding parameters.
3. **Curve Fitting & Analytical Validation:** The baseline of the spectrum is roughly quadratic. To isolate the background from the central spectral peak, select only the smoothed data points where `wavelength < 4002.0` or `wavelength > 4008.0`. 
   Fit a quadratic baseline to these outer regions. You MUST calculate the coefficients analytically using the Ordinary Least Squares (OLS) matrix formula: $\beta = (X^T X)^{-1} X^T y$. 
   *Warning:* The wavelengths are around 4000 nm. Using raw wavelength values will construct a design matrix $X$ that is near-singular, causing `(X^T X)` inversion to fail or produce garbage floating-point errors. To resolve this, you must normalize the independent variable for the baseline fit: define $x_{norm} = \text{wavelength} - 4005.0$. 
   Construct your design matrix $X$ with columns for $1$, $x_{norm}$, and $x_{norm}^2$.
4. **Signal Extraction:** Once you have the baseline coefficients $(c_0, c_1, c_2)$ for the normalized equation $y = c_0 + c_1 x_{norm} + c_2 x_{norm}^2$, compute the predicted baseline for *all* wavelengths. Subtract this baseline from the *smoothed* intensity curve.
5. **Analytical Validation:** Integrate the baseline-subtracted signal over the entire wavelength range to find the total signal area. Use the composite trapezoidal rule (`numpy.trapz`).
6. **Workflow Orchestration:** Write this entire pipeline into a Jupyter Notebook saved at `/home/user/fit_spectrum.ipynb`. 
7. The final cell of your notebook must write the results to `/home/user/fit_results.json` in the following format:
```json
{
  "c0": 10.1234,
  "c1": 2.1234,
  "c2": 0.5123,
  "peak_area": 62.1234
}
```
8. After creating the notebook, run it headlessly in the terminal using `jupyter nbconvert --execute --to notebook --inplace /home/user/fit_spectrum.ipynb` (or an equivalent runner like `papermill`) to ensure the pipeline executes completely and generates the JSON file.

Ensure your code is clean, handles the matrix inversion mathematically (e.g., `np.linalg.inv`), and accurately propagates the normalization shift.