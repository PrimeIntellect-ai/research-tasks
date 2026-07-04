You are a data scientist taking over a project from a former colleague. They left behind a compiled, stripped Linux binary called `/app/signal_processor` which takes noisy time-series data, extracts its spectral features, and compares it to a simulated Monte Carlo baseline. 

Unfortunately, the original source code was lost. We need to integrate this logic into a larger Python pipeline. Your task is to write a Python script at `/home/user/fitter.py` that reads from `stdin` and produces the EXACT SAME OUTPUT as `/app/signal_processor` for any valid input.

Here is the high-level algorithm the binary is known to implement (found in some old notes):
1. **Input**: Read exactly 64 floating-point numbers from standard input (separated by whitespace). This represents our time-domain signal.
2. **Spectral Analysis**: Compute the Discrete Fourier Transform (DFT) of this 64-point sequence. Find the magnitude of each frequency bin.
3. **Normalization**: Normalize the 64 magnitudes so they sum to 1.0. This creates a probability distribution $P$.
4. **Monte Carlo Baseline**: 
   - Extract the normalized magnitude of the DC component (index 0), multiply by 10000, and floor it to an integer. Use this integer to seed a pseudo-random number generator.
   - Run a Monte Carlo simulation with 100,000 iterations. In each iteration, generate a random integer uniformly distributed between 0 and 63 (inclusive). 
   - Calculate the empirical distribution $Q$ (frequencies of each integer 0-63 divided by 100,000).
5. **Distribution Distance**: Compute the Total Variation Distance (TVD) between $P$ and $Q$. The formula for TVD is $\frac{1}{2} \sum_{i=0}^{63} |P_i - Q_i|$.
6. **Output**: Print the TVD to standard output, formatted to exactly 6 decimal places (e.g., `0.123456`).

*Hints:* 
- The binary was written in C and compiled on this system. You will need to think carefully about how standard C library PRNGs (like `srand` and `rand`) behave if you want to achieve identical Monte Carlo baselines in Python. Python's `random` module uses a different algorithm than C's `rand()`.
- Your Python script should be executable and read the 64 floats directly from `sys.stdin`.

Verify your work by passing random sequences of 64 floats to both `/app/signal_processor` and `python3 /home/user/fitter.py` and ensuring the printed strings match perfectly.