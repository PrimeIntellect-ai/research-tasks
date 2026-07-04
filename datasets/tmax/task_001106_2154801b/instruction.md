As a researcher in our computational physics lab, I need you to process some noisy oscillatory data from our recent simulation. 

We have a dataset located at `/home/user/signal.csv`. The file has two comma-separated columns: time `t` (in seconds) and signal `y`. We know the underlying physical model follows the equation:
`y(t) = A * cos(2 * pi * f * t + phi)`

However, the data is corrupted by noise. I need you to write a Go program (`/home/user/analyze.go`) that does the following:
1. Reads the experimental data into appropriate array/slice structures.
2. Performs a Discrete Fourier Transform (DFT or FFT) to find the dominant integer frequency `f` (in Hz). You can assume `f` is an integer between 1 and 20.
3. Uses a numerical optimization algorithm (like gradient descent) to find the optimal amplitude `A` (where A > 0) and phase `phi` (where -pi < phi <= pi) that minimizes the Mean Squared Error (MSE) between the model and the data.
4. Outputs the final parameters to `/home/user/result.json` in exactly this format:
   `{"f_peak": <int>, "A": <float_rounded_to_2_decimals>, "phi": <float_rounded_to_2_decimals>}`

Please ensure you use Go as the primary language to implement the data reading, spectral analysis, and optimization. You may use standard Go libraries or write the DFT and gradient descent from scratch (since the dataset is small, N=100, naive $O(N^2)$ DFT is perfectly acceptable).

Execute your Go program so that `/home/user/result.json` is generated.