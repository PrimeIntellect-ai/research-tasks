I am a researcher running parallel simulations of a vibrating mechanical system. I have collected noisy time-series data from 100 sensors, each recorded for 1024 time steps at a sampling rate of 1024 Hz. The data is stored as a 2D numpy array of shape (100, 1024) in `/home/user/sensor_data.npy`.

I need you to write an MPI-parallelized Python script using `mpi4py` to analyze this data. Please write the script at `/home/user/analyze.py` and ensure it runs successfully with `mpirun -n 4 python3 /home/user/analyze.py`. You may need to install `mpi4py`, `scipy`, `numpy`, and `matplotlib`.

The script must perform the following tasks:
1. **Parallel FFT Analysis**: Load the data and distribute the 100 sensors evenly across the 4 MPI ranks (25 sensors per rank). Each rank should compute the real FFT (`np.fft.rfft`) for its assigned sensors to find the dominant (peak) frequency of each sensor. The sampling spacing `d` is `1/1024`.
2. **Gathering**: Gather all 100 peak frequencies to Rank 0.
3. **Statistical Hypothesis Comparison**: On Rank 0, perform a Shapiro-Wilk test (`scipy.stats.shapiro`) on the 100 peak frequencies to test the null hypothesis that the peak frequencies are normally distributed.
4. **Matrix Decomposition**: On Rank 0, perform a Singular Value Decomposition (SVD) on the entire 100x1024 data matrix to find the principal modes of vibration. Extract the top 3 singular values.
5. **Visualization**: On Rank 0, plot the first principal component (the first row of the `Vh` matrix from the SVD) across the 1024 time steps, and save it to `/home/user/mode1.png`.
6. **Results Export**: On Rank 0, save the numerical results to a JSON file at `/home/user/results.json` with the following structure:
```json
{
  "top_3_singular_values": [float, float, float],
  "shapiro_p_value": float,
  "mean_peak_frequency": float
}
```

Ensure the JSON keys exactly match the above. Keep all computations in double precision (float64).