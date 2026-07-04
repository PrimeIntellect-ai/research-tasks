You are a data scientist debugging a numerical integrator that is used across a network of 50 spatial nodes. The integrator diverged, creating a strong high-frequency artifact, but the raw data is extremely noisy.

You have been provided with the raw simulation output in `/home/user/sensor_data.csv`. The file contains a matrix of 50 rows (nodes) and 1024 columns (time steps) without headers. 

Your task is to isolate the temporal artifact and quantify its prominence. Write a Bash script at `/home/user/analyze.sh` that processes this data (you may invoke an inline Python script or create a separate Python file to be called by your Bash script) to perform the following steps:

1. Load the CSV into a NumPy array $X$.
2. Perform Singular Value Decomposition (SVD) on $X$ such that $X = U \Sigma V$. Extract the first principal temporal component (the first row of $V$, i.e., $V[0, :]$).
3. Compute the power spectrum of this temporal component using the Real Fast Fourier Transform (`numpy.fft.rfft`). The power is the squared magnitude of the complex FFT output.
4. Ignore the DC component by setting the power at index 0 to exactly 0.
5. Identify the frequency bin (index) with the maximum power.
6. Calculate the Z-score of this maximum peak power relative to the entire power spectrum array (using the population mean and standard deviation of the modified power spectrum).
7. Save the integer index of the peak frequency to `/home/user/peak_freq.txt`.
8. Save the Z-score of the peak frequency, rounded to 2 decimal places, to `/home/user/zscore.txt`.

Ensure your Bash script is executable and runs the complete pipeline when invoked as `bash /home/user/analyze.sh`.