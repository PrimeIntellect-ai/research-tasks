You are an expert performance engineer tasked with analyzing high-frequency application latency traces to detect systemic anomalies. We have been collecting execution latency traces from our production microservices.

There are two main objectives:

**Part 1: Fix the Profiling Package**
We have a proprietary Python package for loading these custom latency traces, vendored at `/app/signal-profiler-0.1.0`. However, the build is currently broken due to a configuration error introduced by a previous developer.
1. Identify and fix the bug in `/app/signal-profiler-0.1.0` so it can be installed.
2. Install the package in the current environment. 

**Part 2: Build an Anomaly Detector**
We have two directories of unlabeled historical traces (though their names indicate their nature for your testing purposes):
- `/app/traces/clean/`: Contains normal execution traces (primarily Gaussian noise).
- `/app/traces/evil/`: Contains anomalous execution traces. These traces suffer from periodic CPU throttling (which manifests as a strong periodic signal in the latency timeseries) and multi-modal latency distributions (bimodal due to cache misses).

Write a Python script at `/home/user/detector.py` that takes a directory of trace files and classifies each as either `"clean"` or `"evil"`.
Your script must be invokable exactly like this:
`python /home/user/detector.py --input-dir <directory_path> --output <output_json_path>`

Your script must:
1. Iterate over all `.csv` files in the provided `--input-dir`.
2. Use the `signal_profiler.load_trace(filepath)` function (from the package you fixed in Part 1) to load the latency timeseries as a NumPy array.
3. Use **Fourier transforms (FFT)** to analyze the spectral density and detect periodic throttling frequencies.
4. Use **Kernel Density Estimation (KDE)** to fit the distribution of the latency values to detect if the distribution is multi-modal.
5. Combine these signals (or use statistical hypothesis comparison against a normal distribution) to classify the trace.
6. Output a JSON file at `--output` containing a dictionary mapping the base filename (e.g., `trace_01.csv`) to the string `"clean"` or `"evil"`.

We will run your script against a hidden evaluation set of clean and evil traces. You must correctly classify 100% of the traces in both sets to succeed. Use the provided `/app/traces/` as your development set.