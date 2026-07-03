You are a machine learning engineer preparing a dataset of genomic signals for a deep learning model. Your raw data consists of DNA sequences and raw nanopore electrical signals, and you need to align the signals using a known primer sequence, then filter them.

We have a proprietary Python package located at `/app/genomic_dsp` that contains optimized routines for this. It provides a `genomic_dsp` module with a `filter_signal(signal_array: list[float]) -> list[float]` function. This function uses Fourier transforms to remove high-frequency noise and matrix decomposition to normalize the signal. 

However, the package currently has a bug. A developer accidentally commented out a critical import in `/app/genomic_dsp/genomic_dsp/transforms.py`. 

Your tasks:
1. Fix the bug in the vendored package at `/app/genomic_dsp` and install it into your environment (e.g., `pip install -e /app/genomic_dsp`).
2. Write a Python script at `/home/user/prepare_data.py` that processes data from standard input (`stdin`).
3. Your script must read line by line. Each line will be a valid JSON object with the following keys:
   - `"primer"`: A short string of DNA (e.g., `"ACGT"`).
   - `"sequence"`: A longer string of DNA.
   - `"signal"`: A list of floats representing the raw electrical signal (length matches the length of `"sequence"`).
4. For each JSON object, your script must:
   a. Find the first exact substring match of the `primer` within the `sequence`. Let the 0-based start index be `start` and the end index (inclusive) be `end`.
   b. If the primer is NOT found in the sequence, print `NO_MATCH` to `stdout`.
   c. If found, slice the `signal` array to extract the segment corresponding to the primer: `sliced_signal = signal[start : end + 1]`.
   d. Pass `sliced_signal` into `genomic_dsp.filter_signal(sliced_signal)`.
   e. The function will return a list of filtered floats. Round each float to exactly 4 decimal places.
   f. Print the rounded floats as a comma-separated string to `stdout` (e.g., `1.2345, -0.0000, 3.1416`).
   
Your script must be robust, executable as `python3 /home/user/prepare_data.py`, and exactly match the required output format. Do not print any extra debugging information to `stdout`.