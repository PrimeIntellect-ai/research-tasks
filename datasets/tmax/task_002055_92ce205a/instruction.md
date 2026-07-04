I have a batch of signal data, but I'm running into reproducibility issues when processing it due to floating-point reduction order in my sums. I need you to write a robust Python script to process these signals, extract their dominant frequencies, and solve a related non-linear physical model.

Please create a script at `/home/user/spectral_solver.py` that performs the following exact steps:

1. Load the 2D numpy array from `/home/user/signal.npy`. This array has a shape of (100, 1024), representing 100 separate time-domain signals of length 1024.
2. Apply a standard Hanning window to each of the 100 signals (multiply each row by `numpy.hanning(1024)`).
3. Compute the Real Fast Fourier Transform (`numpy.fft.rfft`) for each windowed signal.
4. Calculate the magnitude (absolute value) of the FFT results.
5. For each signal, find the index of the frequency bin with the maximum magnitude. Let's call this array of 100 peak indices $P$.
6. For each peak index $p \in P$, solve the non-linear equation $y + e^{y/100} = p$ for $y$. Use a starting guess of $y = p$. (You can use `scipy.optimize.fsolve` or `scipy.optimize.root`).
7. You must ensure strict floating-point reproducibility. Take the 100 solutions for $y$, **sort them in ascending order**, and save this sorted 1D numpy array to `/home/user/solutions.npy`.
8. Calculate the mean of these 100 solutions. To avoid reduction order variations, you must compute the sum of the **sorted** array using standard sequential addition (or `math.fsum`), then divide by 100.
9. Write this mean value, formatted to exactly 6 decimal places (e.g., `123.456789`), to a file named `/home/user/result.txt`.

You can run your script to verify it works. The goal is to produce the correct `/home/user/solutions.npy` and `/home/user/result.txt`.