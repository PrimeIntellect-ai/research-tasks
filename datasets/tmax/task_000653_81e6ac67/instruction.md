You are an AI assistant helping a data scientist analyze a noisy time-series dataset from a recent spectroscopy experiment. 

The raw data is located at `/home/user/spectroscopy_data.csv`. It contains two columns: `time` (in seconds) and `amplitude` (in arbitrary units). The sampling rate is 200 Hz.

The scientist has two competing hypotheses regarding the true emission frequencies of the sample:
*   **Hypothesis A:** The signal contains primary frequencies at 10 Hz, 25 Hz, and 50 Hz.
*   **Hypothesis B:** The signal contains primary frequencies at 10 Hz, 20 Hz, and 50 Hz.

Previous attempts to analyze this data yielded non-reproducible results due to differences in chunking and floating-point summation orders. To fix this, you need to write a standardized Python script `/home/user/analyze_spectrum.py` that strictly follows this procedure:

1. **Read the data**: Load `/home/user/spectroscopy_data.csv`.
2. **Compute the Power Spectral Density (PSD)**: Use `scipy.signal.welch` on the `amplitude` column. You must use the exact following parameters to ensure strict reproducibility:
    *   `fs=200.0`
    *   `window='hann'`
    *   `nperseg=1024`
    *   `noverlap=512`
    *   `detrend='constant'`
    *   `return_onesided=True`
    *   `scaling='density'`
3. **Statistical Hypothesis Comparison**: 
    *   For **Hypothesis A**, sum the PSD values for all frequency bins that fall *strictly inside* the inclusive ranges: `[9.0, 11.0]`, `[24.0, 26.0]`, and `[49.0, 51.0]`.
    *   For **Hypothesis B**, sum the PSD values for all frequency bins that fall *strictly inside* the inclusive ranges: `[9.0, 11.0]`, `[19.0, 21.0]`, and `[49.0, 51.0]`.
4. **Determine the Best Model**: The model with the higher total power in its defined frequency bands is the winner.
5. **Output**: Save the results to `/home/user/hypothesis_result.json` in the following exact format:
```json
{
  "power_A": <float>,
  "power_B": <float>,
  "best_model": "<'A' or 'B'>"
}
```

Ensure your script is self-contained and runs without errors. Install any required Python packages (like `numpy`, `scipy`, `pandas`) using pip before running your script.