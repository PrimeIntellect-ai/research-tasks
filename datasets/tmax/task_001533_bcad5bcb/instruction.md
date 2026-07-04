You are a performance engineer investigating non-reproducible jitter in our distributed simulation system. To analyze this, we perform spectral analysis on latency logs. 

We have a proprietary Python package `fast-stat-profiler` located at `/app/fast-stat-profiler-1.0`. However, the previous maintainer left a bug in it: the `setup.py` attempts to compile a C-extension but the `Makefile` invokes `python setup.py install` instead of `python3 setup.py install`, which fails in our modern environment. Furthermore, the package requires the environment variable `ALLOW_PROFILER_BUILD=1` to be set during compilation, which is currently undocumented.

Your task has two parts:
1. Fix the build process of the `fast-stat-profiler` package in `/app/fast-stat-profiler-1.0` and install it system-wide or in the user environment so it can be imported as `fast_stat_profiler`.
2. Write a Python script at `/home/user/analyze_jitter.py` that does the following:
   - Reads lines from standard input (stdin). Each line is a comma-separated string, e.g., `timestamp_ms,latency_ms`.
   - Discards the timestamp and extracts the `latency_ms` column as a sequence of floats.
   - Reshapes/cleans the sequence using the vendored package by calling `fast_stat_profiler.clean_latency(latency_list)`. This function returns a cleaned NumPy array.
   - Computes the Discrete Fourier Transform (DFT) of the cleaned latency array using `numpy.fft.fft`.
   - Computes the magnitude of each frequency component.
   - Ignores the DC component (index 0).
   - Finds the top 3 frequency indices with the highest magnitudes. In case of a tie in magnitude, prioritize the smaller frequency index.
   - Prints these top 3 indices and their magnitudes to standard output (stdout), rounded to 4 decimal places, in the following exact format:
     `Idx: {index}, Mag: {magnitude:.4f}`

For example, your output should look exactly like:
Idx: 5, Mag: 12.3456
Idx: 2, Mag: 9.8765
Idx: 14, Mag: 8.0000

Ensure your script handles arbitrary lengths of input (up to 10,000 lines) and strictly matches the expected output format. The script will be tested against a variety of inputs by an automated fuzzer.