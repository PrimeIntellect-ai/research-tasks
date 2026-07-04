You are a data scientist fitting a frequency model to a noisy sensor signal. You need to validate the robustness of your dominant frequency estimation, check the numerical stability of an analytical transformation model, and ensure the current FFT implementation passes a regression test against a legacy output.

All your work should be orchestrated using a Bash script. 

Write a Bash script named `/home/user/validate_pipeline.sh` that performs the following steps and writes the results to `/home/user/report.txt`.

**Available Files (already in `/home/user/`):**
1. `signal.dat`: A space-separated file containing the original sensor data. Column 1 is time, Column 2 is the signal value.
2. `fft.py`: A Python script that reads space-separated `time value` data from standard input (stdin) and prints a single floating-point number representing the dominant frequency.
3. `legacy_fft.out`: A text file containing the expected dominant frequency from a previous, highly-trusted pipeline.
4. `analytical_model.py`: A Python script that takes a single floating point argument `x` and prints a transformed value.

**Tasks your script must perform:**

**1. Scientific Code Regression Testing:**
Pipe `signal.dat` into `fft.py` to get the baseline dominant frequency. Compare this baseline frequency to the value in `legacy_fft.out`. If the absolute difference is less than `0.01`, the regression test passes.

**2. Parametric Bootstrap Confidence Intervals & Spectral Analysis:**
To find the 90% confidence interval of the frequency peak, perform a parametric bootstrap in Bash:
- Loop 100 times.
- In each iteration, use `awk` to inject random uniform noise in the range `[-0.5, 0.5]` to the *signal value* (Column 2) of `signal.dat`. (Keep Column 1 unchanged).
- Pipe this noisy dataset into `fft.py` and record the dominant frequency.
- Sort the 100 frequency results in ascending order.
- Determine the 90% confidence interval by extracting the 5th value (lower bound) and the 95th value (upper bound) from the sorted list.

**3. Numerical Stability Testing:**
The analytical model processes a critical parameter $x$. Test its stability at $x = 1.0$.
- Run `python analytical_model.py 1.0`
- Run `python analytical_model.py 1.00000001`
- Calculate the absolute difference between the two outputs. If the difference is greater than `1.0`, the model is considered numerically unstable.

**Output Format:**
Your script must create `/home/user/report.txt` exactly in the following format:
```
REGRESSION: <PASS or FAIL>
BOOTSTRAP_CI_90: [<lower_bound>, <upper_bound>]
STABILITY: <PASS or FAIL>
```
*(Note: Replace the bracketed placeholders with your computed values).*

Ensure your script has executable permissions and run it to produce the final `report.txt`.