You are an ML engineer preparing training data from a network of chemical sensors. 

The raw spectroscopy data is served by a local multi-service architecture, but it is heavily corrupted by baseline drift and overlapping signals. A naive matrix factorization applied directly to this data fails to isolate the true underlying chemical components because the input matrix is near-singular and dominated by noise.

Your task is to fix the processing pipeline:
1. Bring up the data services by running `/app/start_services.sh`. This will start a Redis instance (port 6379) and a Flask-based Data Service (port 5000).
2. The raw data can be fetched via a GET request to `http://127.0.0.1:5000/data`. It returns a JSON object with a `spectra` key containing a 2D array (1000 samples x 200 wavelength bins).
3. Write a Python script `/home/user/process.py` to fetch this data and preprocess it. Use a Savitzky-Golay filter (from `scipy.signal`) with a window length of 21, polynomial order of 3, and compute the second derivative (`deriv=2`) along the wavelength axis to remove the baseline drift and sharpen the peaks.
4. Take the absolute value of the filtered data to ensure non-negativity.
5. Perform Non-negative Matrix Factorization (NMF) with 3 components (from `sklearn.decomposition`) on this preprocessed data to extract the pure component spectra.
6. Identify the primary peak position (the index of the maximum value) for each of the 3 components.
7. To provide analytical validation, implement a reproducible computation pipeline that calculates the 95% bootstrap confidence intervals for these peak positions. Create 100 bootstrap samples of the preprocessed data matrix (resampling rows with replacement), re-run NMF, extract the peaks, and sort them. Compute the 2.5th and 97.5th percentiles for the 1st, 2nd, and 3rd peak indices.
8. Save the results to `/home/user/result.json` in the following exact format, with the components sorted by their mean peak index in ascending order:

```json
{
  "peaks": [
    {
      "mean_index": 42.1,
      "ci_lower": 40.0,
      "ci_upper": 44.0
    },
    ...
  ]
}
```

Make sure your processing script runs successfully and writes the correct output. You have full access to standard Python scientific libraries (`numpy`, `scipy`, `scikit-learn`, `requests`).