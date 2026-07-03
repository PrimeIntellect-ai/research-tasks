You are an AI assistant helping a machine learning engineer prepare a training dataset of simulated harmonic oscillator trajectories.

Some of our simulation runs produced unstable, non-reproducible results due to floating-point reduction order issues during parallel execution. We need to filter out these bad trajectories before training.

I have provided an image at `/app/criteria.png` which contains the mathematical formulation of the energy invariant and the exact numerical differentiation scheme and threshold you must use to detect instability. 

Your task:
1. Extract the filtering criteria and numerical scheme from `/app/criteria.png`. (You may use OCR tools like `tesseract`, which is available, or inspect it).
2. Set up your Go environment and install any necessary C-libraries for reading NetCDF-4 files (`.nc`). 
3. Write a Go program at `/home/user/filter.go` that implements the classifier. 
4. The Go program must take a single command-line argument (the path to a NetCDF file).
   - If the file meets the criteria (it is stable/clean), the program must exit with code `0`.
   - If the file violates the criteria (it is unstable/evil), the program must exit with code `1`.

The NetCDF files contain the following 1D variables (arrays of length N):
- `t`: Time steps (float64)
- `x`: Position (float64)
- `v`: Velocity (float64)

The time step `dt` is constant and can be derived from `t[1] - t[0]`.

To pass, your program will be tested against two hidden corpora:
- A clean corpus of valid NetCDF files (must all exit 0).
- An evil corpus of corrupted NetCDF files (must all exit 1).

Make sure your Go code builds successfully and has the exact entry point signature:
`go run /home/user/filter.go <path-to-nc-file>`