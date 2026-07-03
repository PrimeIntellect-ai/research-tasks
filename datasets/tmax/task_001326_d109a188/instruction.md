You are an ML engineer preparing a large-scale training dataset of noisy spectroscopic signals (1024 points per spectrum). 

Your team previously used a proprietary C++ tool to clean the data before feeding it into the model. However, this tool is too slow for the new 10-million sample dataset. You need to write a fast, equivalent Python pipeline that mimics its exact signal processing steps.

We have provided a subset of the raw data and the legacy compiled tool for you to study:
- Raw spectra: `/app/raw_spectra.csv` (100 rows, each containing 1024 comma-separated float values representing intensities).
- Legacy cleaner: `/app/legacy_cleaner` (a stripped, black-box binary).
  - Usage: `/app/legacy_cleaner <input_csv> <output_csv>`

Your task is to reverse-engineer the signal processing pipeline applied by `/app/legacy_cleaner` and implement an equivalent, optimized Python script.

Requirements:
1. Create a Python script at `/home/user/process_spectra.py`.
2. The script must take two CLI arguments: `python process_spectra.py <input.csv> <output.csv>`.
3. It must read the 1024-point spectra, apply the exact same Fourier transform (FFT) smoothing and baseline correction as the legacy binary, and save the cleaned spectra to the output CSV.
4. Additionally, the script must calculate the 95% bootstrap confidence interval (using 1000 resamples, percentile method) of the **maximum peak heights** (one max value per cleaned spectrum) across the entire dataset processed.
5. The script must output this confidence interval to a JSON file at `/home/user/stats.json` in the following format:
   ```json
   {
     "ci_lower": 1.234,
     "ci_upper": 5.678
   }
   ```

To succeed, you must carefully analyze the input and output of the legacy tool to figure out its exact cutoff frequencies for the FFT filter and its baseline subtraction mathematical model, then replicate them in your script. We will evaluate your script on a hidden, held-out dataset to measure its Mean Squared Error (MSE) against the legacy tool's output.