I am building a reproducible computation pipeline for primer design and sequence alignment, but I'm running into an issue with a locally vendored scientific package. 

I have a custom C-extension package called `primer_score` located at `/app/primer_score-0.1.0`. When I try to install it using `pip install -e .`, the compilation fails due to an unrecognized compiler flag error.

Please do the following:
1. Diagnose and fix the compilation issue in the `primer_score` package source code (look at the compiler flags being passed).
2. Install the fixed package into the system Python environment.
3. Write a Python script at `/home/user/analyze_primer.py` that takes a single DNA sequence (string of A, C, G, T) as its first command-line argument (`sys.argv[1]`).

The script must perform the following numerical analysis:
- Pass the sequence to the package function `primer_score.compute_affinity(sequence)`. This returns a list of float values representing the thermodynamic affinity at each position $i$, array $A$ of length $L$.
- Compute the forward finite difference of this array to find the derivative profile: $D[i] = A[i+1] - A[i]$ for $i = 0, \dots, L-2$.
- Compute the numerical integral of the **absolute values** of $D$ using the Trapezoidal rule over a uniform grid with spacing 1. The formula to use is:
  $\text{Integral} = \sum_{i=0}^{L-3} \frac{|D[i]| + |D[i+1]|}{2}$
- Print *only* the final integrated value to standard output, formatted to exactly 4 decimal places (e.g., `12.3456`).

Your script will be tested against a strict regression testing oracle with thousands of random sequences to ensure bit-exact output equivalence.