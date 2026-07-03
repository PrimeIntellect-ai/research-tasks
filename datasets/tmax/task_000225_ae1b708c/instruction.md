A previous graduate student left behind an incomplete pipeline for calculating the spectral power of molecular trajectories. Our results have been highly inconsistent across different cluster architectures due to floating-point addition non-associativity when computing the total spectral power.

We need you to build a robust Go utility that implements this calculation deterministically.

You have been provided an image at `/app/window_spec.png`. It contains two critical pieces of mathematical information:
1. The exact formula for the spectral windowing function that must be applied to the sequence before transforming.
2. The exact summation algorithm you must use to accumulate the total power (this specific algorithm minimizes floating-point accumulation errors, which is the source of our non-reproducibility).

Here is the exact specification of the tool you must write:
- The tool must read from standard input (`stdin`).
- The input will consist of multiple lines. You must extract only the lines that begin with the exact string `ATOM`. 
- Valid `ATOM` lines will contain exactly 5 whitespace-separated tokens: `ATOM`, an integer ID, and three 64-bit floats representing X, Y, and Z coordinates. Ignore any line that does not strictly match this format or fails to parse.
- Extract the Z coordinate into a sequence $Z$ of length $N$.
- If $N=0$, simply print `0.000000` and exit.
- Apply the window function (from `/app/window_spec.png`) to the sequence $Z$. If $N=1$, the window value is $1.0$.
- Compute the standard 1D Discrete Fourier Transform (DFT) of the windowed $Z$ sequence to get complex array $X_k$. (Do not use an FFT library; implement the naive $O(N^2)$ DFT formula: $X_k = \sum_{n=0}^{N-1} Z_n \cdot e^{-i 2\pi k n / N}$).
- Calculate the squared magnitude $|X_k|^2 = Re(X_k)^2 + Im(X_k)^2$ for each frequency bin $k \in [0, N-1]$.
- Sum all the squared magnitudes using the specific summation algorithm named in `/app/window_spec.png` to guarantee reproducible floating-point accumulation.
- Print the final accumulated sum to standard output, formatted to exactly 6 decimal places (e.g., `12.345678`), with a trailing newline.

Write your Go source code in `/home/user/dft_tool.go` and compile it to an executable at `/home/user/dft_tool`.