You are a researcher running simulations for an array of sensors. The raw simulation outputs are stored in FITS format. You need to write a Go program to process these files concurrently, perform spectral analysis, solve a calibration equation, and extract statistical properties.

Your task is to create and run a Go program at `/home/user/analyze.go` that does the following:

1. **Parallel Processing**: Read all FITS files located in `/home/user/data/` concurrently using goroutines. The files are named `sensor1.fits`, `sensor2.fits`, `sensor3.fits`, and `sensor4.fits`.
2. **Scientific Data I/O**: Use the Go library `github.com/astrogo/fitsio` to read the files. Each FITS file contains a Primary HDU (empty) and a Binary Table in the first extension. Extract the float64 data from the column named `FLUX`. The length of the data is guaranteed to be 1024.
3. **Fourier Transform**: Use `github.com/mjibson/go-dsp/fft` to compute the 1D Fast Fourier Transform (FFT) of the `FLUX` array for each sensor.
4. **Analysis & Equation Solving**:
   - Calculate the magnitude (absolute value) of the complex FFT output.
   - Find the index $k$ (where $0 < k \le 512$) that corresponds to the maximum FFT magnitude (the dominant frequency index).
   - The sensor has a linear calibration curve: $3.5x - 12.0 = k$. Solve this linear equation for $x$ to find the `CalibratedFreq`.
5. **Statistical Extraction**:
   - Compute the mean of the FFT magnitudes, **excluding** the DC component (index 0). So, average over indices 1 to 1023. Let this be `MeanMagnitude`.
6. **Output**: Write the results to `/home/user/results.json`. The JSON file should be an object where the keys are the filenames (e.g., `"sensor1.fits"`) and the values are objects with the keys `"calibrated_freq"` (float) and `"mean_magnitude"` (float).

Constraints:
- Initialize your Go module in `/home/user` (e.g., `go mod init analyze`).
- Run `go mod tidy` to fetch dependencies.
- Ensure the output JSON is formatted properly and contains the exact keys specified.
- The `mean_magnitude` should be calculated accurately (sum of magnitudes for index 1 to 1023, divided by 1023).