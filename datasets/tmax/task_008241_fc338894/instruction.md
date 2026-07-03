You are helping a computational researcher debug a data pipeline. They are running simulations based on observational sensor data. However, the downstream matrix factorization step frequently fails due to ill-conditioned (near-singular) matrices caused by massive DC offsets in certain sensor recordings.

You need to write a Go program that acts as a reproducible data-reshaping and spectral analysis pipeline to identify these problematic files.

The raw data is located in `/home/user/sensor_data/`. There are multiple CSV files. Each CSV contains a `timestamp` and a `value` column, but the data is messy: it contains comment lines starting with `#`, empty lines, and the first row is a header.

Write a Go program located at `/home/user/analyze.go` that does the following:
1. Initializes a Go module (`go mod init analyzer` and `go get github.com/mjibson/go-dsp/fft` is recommended for the FFT, but you may use any valid approach).
2. Takes the data directory path as a command-line argument.
3. Reads and cleans the observational data from all CSV files in the directory. You MUST process the files concurrently using Go routines (e.g., using a wait group or channels).
4. For each file, extracts the `value` column (as `float64`) in order. Assume each valid file has exactly 256 valid data points after cleaning.
5. Performs a 1D Fast Fourier Transform (FFT) on the sequence of values.
6. Calculates the magnitude of each complex frequency component.
7. Identifies the "Dominant Frequency Index", which is the index (from 1 to 127) with the highest magnitude. **Ignore index 0 (the DC component) when finding the dominant frequency.**
8. Checks for the "Near-Singular" condition: If the magnitude of the DC component (index 0) is strictly greater than 50.0 times the magnitude of the Dominant Frequency, the file is flagged as `SINGULAR`. Otherwise, it is `STABLE`.
9. Writes the results to `/home/user/results.txt`. 

The output file `/home/user/results.txt` must have exactly one line per file processed, sorted alphabetically by filename, in this exact format:
`[filename]: [FLAG] [dominant_frequency_index]`

Example of expected lines in `/home/user/results.txt`:
```
data_00.csv: STABLE 12
data_01.csv: SINGULAR 5
```

Once you have written the program, compile and run it against the `/home/user/sensor_data/` directory to produce the `/home/user/results.txt` file.