You are helping a data scientist debug a model fitting pipeline for spectroscopy data. We have noticed non-reproducible energy measurements across different environments because our previous Python scripts accumulated floating-point arrays in non-deterministic orders (like parallel map-reductions). 

Your task is to write a deterministic, reproducible spectral smoothing and integration tool in Go.

You have been provided an image at `/app/filter_spec.png` that contains the mathematical specification for our 5-point smoothing filter and the final spectral energy formula.

Requirements for your Go program:
1. Extract the filter coefficients and boundary conditions from `/app/filter_spec.png`.
2. Read a single line of space-separated floating-point numbers from standard input. These represent the raw input signal $x$.
3. Apply the 5-point smoothing filter to produce the smoothed signal $y$.
4. Calculate the Spectral Energy $E$ as specified in the image.
5. **CRITICAL for reproducibility:** To prevent floating-point reduction order differences, you MUST accumulate the sum for the Spectral Energy sequentially in a single `float64` variable, starting strictly from index $i=0$ up to $N-1$, adding exactly one $y_i^2$ term at a time.
6. Print the final energy $E$ to standard output formatted to 8 decimal places (e.g., `fmt.Printf("%.8f\n", E)`).

Implementation constraints:
- Save your Go source code at `/home/user/process_spectrum.go`.
- Compile it to an executable at `/home/user/process_spectrum`.
- Ensure it uses only standard library packages.

An automated verifier will pipe thousands of randomized signal arrays into your executable and assert bit-for-bit equivalence with our reference C-based oracle.