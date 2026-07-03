You are an ML engineer preparing a spectroscopy training dataset. Our models are highly sensitive to numerically unstable signals, baseline artifacts, and non-physical derivatives, so you need to create a robust data sanitization pipeline.

We process signals using an internal proprietary package called `spectro-tools`. However, the current vendored source code for this package has a bug preventing it from functioning correctly, and our build server is disconnected from the internet. 

Your task consists of two parts:

**Part 1: Fix and Install `spectro-tools`**
1. The source code for `spectro-tools` version `0.4.2` is located at `/app/spectro-tools-0.4.2`.
2. Find and fix the bug in the package source that prevents the `baseline.py` module from executing properly. (It currently fails during execution with a missing reference/import error when `remove_baseline` is called).
3. Install the package locally in your environment. NO INTERNET access is available. 

**Part 2: Develop the Sanitization Script**
Write a Python script at `/home/user/sanitize_data.py` to classify spectroscopy signals as valid (ACCEPT) or invalid (REJECT).
1. The script should be executable via the command line and take a target directory containing `.csv` signal files as an argument:
   `python /home/user/sanitize_data.py --input-dir <path_to_directory>`
2. Each `.csv` file contains two columns: `wavelength` and `intensity`.
3. For each file, the script must:
   - Load the signal.
   - Use `spectro_tools.baseline.remove_baseline(intensity)` to compute the baseline-corrected signal.
   - Perform numerical stability testing: compute the first derivative of the baseline-corrected intensity with respect to wavelength. 
   - Perform analytical validation: check for analytical impossibilities such as `NaN` or `Inf` values resulting from the baseline correction.
4. **Rejection Criteria (Evil Signals):**
   - The signal must be REJECTED if `remove_baseline` produces any `NaN` or `Inf` values.
   - The signal must be REJECTED if the absolute value of the first derivative of the baseline-corrected signal exceeds `50.0` at any point (indicating a non-physical high-frequency artifact or instability).
5. **Acceptance Criteria (Clean Signals):**
   - If the signal passes all stability and analytical checks, it must be ACCEPTED.
6. The script must write its classification results to `/home/user/classification.log`. Each line must precisely match the format:
   `FILENAME: ACCEPT` or `FILENAME: REJECT`
   (e.g., `signal_001.csv: ACCEPT`).

We will test your script against two separate, hidden corpora of spectroscopy signals. It must perfectly separate the clean data from the corrupted data.