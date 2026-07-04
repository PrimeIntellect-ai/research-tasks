You are a platform engineer optimizing a CI/CD pipeline step that processes audio signals. A recent pipeline bottleneck has been traced to a pure Python implementation of a custom mathematical digital signal processing (DSP) algorithm—specifically, a naive time-domain convolution filter. 

Your task is to optimize this bottleneck using C-bindings (FFI) to meet our CI performance thresholds.

We have provided a slow, pure-Python implementation of a convolution filter. You need to:
1. Translate the core mathematical convolution logic into C.
2. Compile the C code into a shared object library (`/home/user/libfilter.so`).
3. Write a Python wrapper (`/home/user/fast_filter.py`) using `ctypes` that exposes the exact same interface as the slow Python version.
4. Process the standard CI audio fixture located at `/app/test_signal.wav` using your fast filter implementation.

Here is the slow Python implementation (reference logic):
```python
# /home/user/slow_filter.py
def slow_convolve(signal: list[float], kernel: list[float]) -> list[float]:
    n = len(signal)
    m = len(kernel)
    result = [0.0] * (n + m - 1)
    for i in range(n):
        for j in range(m):
            result[i + j] += signal[i] * kernel[j]
    return result
```

Your `fast_filter.py` must contain a function `fast_convolve(signal_array, kernel_array)` which takes `numpy` arrays of type `float32` (or standard lists, but `numpy` arrays are recommended for FFI speed) and returns the convolved array.

Next, write a benchmarking and verification script at `/home/user/benchmark.py` that:
1. Reads `/app/test_signal.wav` (which is a mono, 16-bit PCM WAV file).
2. Normalizes the audio data to floats between -1.0 and 1.0.
3. Generates a smoothing kernel: an array of 500 ones divided by 500 (`[0.002] * 500`).
4. Runs both `slow_convolve` and `fast_convolve` on the audio data.
5. Verifies that the Mean Squared Error (MSE) between the two outputs is less than `1e-5`.
6. Prints the execution time of both, calculating the speedup factor: `Speedup = Time_Slow / Time_Fast`.

Write the outputs to `/home/user/benchmark_results.txt` in exactly this format:
```
MSE: <mse_value>
Speedup: <speedup_value>
```

Your C implementation must yield a speedup of **at least 50.0x**.
Use standard system tools (gcc, python3, pip, venv) to manage dependencies and build the code.