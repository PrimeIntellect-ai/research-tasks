You are assisting a data scientist who is trying to fit a low-dimensional model to a noisy time series. The current numerical integration steps keep diverging because high-frequency noise in the data causes the singular value decomposition (SVD) of the system's trajectory matrix to blow up.

We need to build a reproducible pipeline to filter the signal and find the optimal frequency cutoff ($f_c$) that yields a dominant singular value closest to a known target threshold.

**Your Goal:**
Write a pipeline consisting of a Bash orchestrator and a Python helper script to perform a grid search over cutoff frequencies.

**Data Details:**
- A time series dataset is located at `/home/user/signal.csv`. It contains 500 rows of a single column of values representing a signal sampled at 100 Hz ($dt = 0.01$ s).

**Workflow Requirements:**
1. Create a Python script `/home/user/compute.py` that takes two arguments: an input CSV file and an integer cutoff frequency $f_c$ (in Hz). This script must:
   - Read the 1D signal.
   - Perform a Fast Fourier Transform (FFT).
   - Zero out all FFT coefficients corresponding to frequencies strictly greater than $f_c$ Hz (both positive and negative frequencies, remembering the Nyquist limits).
   - Perform an Inverse FFT to get the filtered real signal.
   - Construct a trajectory matrix (Hankel matrix) from the filtered signal with a window length $L = 50$. (Row 1 is $x_0 \dots x_{49}$, Row 2 is $x_1 \dots x_{50}$, up to the end of the signal).
   - Compute the Singular Value Decomposition (SVD) of this Hankel matrix.
   - Print *only* the largest singular value ($\sigma_1$) to standard output as a float.

2. Create a Bash script `/home/user/optimize.sh` that takes a target singular value as its first argument (e.g., `./optimize.sh 150.5`). This script must:
   - Contain the optimization loop written purely in Bash.
   - Iterate over integer cutoff frequencies $f_c \in \{1, 2, 3, \dots, 20\}$.
   - For each $f_c$, invoke `compute.py` to get the dominant singular value.
   - Keep track of which $f_c$ produces a singular value with the smallest absolute difference from the target singular value.
   - Once the loop finishes, write the single best integer $f_c$ to `/home/user/best_fc.txt`.

**Execution:**
Run your Bash script with a target singular value of `85.0`:
`bash /home/user/optimize.sh 85.0`

**Constraints:**
- The grid search loop, comparison logic, and final file writing must be written in the Bash script (`optimize.sh`), not Python. Python should only be used as a mathematical subroutine.
- Use `numpy` or `scipy` for the FFT and SVD operations.