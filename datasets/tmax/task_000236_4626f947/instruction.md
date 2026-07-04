You are an AI assistant helping a data scientist analyze noisy spectroscopy data. 

The scientist has a dataset of spectral measurements located at `/home/user/spectra.csv`. The file has two comma-separated columns with headers: `wavelength` (in nm) and `intensity` (arbitrary units). 

Your task is to write a Go program `/home/user/analyze.go` that estimates the peak emission wavelength and calculates its 95% confidence interval using a parallelized Monte Carlo Bootstrap method. 

Specific requirements for `/home/user/analyze.go`:
1. **Data Reading & Filtering**: Read `/home/user/spectra.csv`. Filter the data to only include rows where the `wavelength` is between `400.0` and `500.0` inclusive. Let $N$ be the number of rows in this filtered dataset.
2. **Peak Estimation**: We estimate the peak position using the Intensity-Weighted Center of Mass (CoM). 
   $CoM = \frac{\sum (wavelength_i \times intensity_i)}{\sum intensity_i}$
3. **Parallel Bootstrap Resampling**:
   - Perform 10,000 bootstrap iterations.
   - Use Go's `goroutines` and `sync.WaitGroup` to distribute the work across multiple concurrent workers (e.g., 4 or 8 workers computing a chunk of the 10,000 iterations).
   - In each iteration, sample $N$ data points *with replacement* from the filtered dataset, and compute the CoM for that bootstrap sample.
   - Collect the 10,000 CoM values.
4. **Confidence Intervals**: 
   - Sort the 10,000 CoM estimates.
   - Calculate the 2.5th percentile (lower bound) and 97.5th percentile (upper bound). (For an array of size 10000, these correspond to indices 250 and 9750 when 0-indexed).
   - Compute the mean of the 10,000 CoM estimates.
5. **Output**: Write the results to `/home/user/peak_ci.json` with the following exact keys and numeric values (do not format as strings):
   ```json
   {
       "mean_com": 450.123,
       "ci_lower": 449.123,
       "ci_upper": 451.123
   }
   ```

After writing the code, compile and run it to produce the `peak_ci.json` file. Ensure your Go code is well-structured and uses the standard library.