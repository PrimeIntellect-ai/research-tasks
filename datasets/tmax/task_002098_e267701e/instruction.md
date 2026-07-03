You are a bioinformatics analyst working on an end-to-end pipeline to discover hidden sequence motifs using MCMC sampling and posterior density estimation. 

You have been provided with the source code for a proprietary, specialized Python package called `seqmotif`, located at `/app/vendored/seqmotif-0.4.2`. This package contains a C-extension that performs high-performance MCMC sampling for density estimation of nucleotide distributions.

However, the package has two critical issues:
1. It currently fails to compile from source due to a misconfigured build file. The C-extension requires math library functions (like `exp` and `log`), but the linker flags in the build configuration are missing the required math library dependency.
2. Even when compiled, the matrix factorization step inside the C code fails (returning NaNs or crashing) on "near-singular" inputs. Specifically, if the input sequence completely lacks a certain nucleotide (e.g., no 'C's), the empirical transition matrix becomes singular. You must find the hardcoded `pseudocount` variable in the C source code and change it from `0.0` to `0.01` to add a ridge/regularization prior.

Your tasks are:
1. **Fix and Install the Package**: Inspect `/app/vendored/seqmotif-0.4.2`. Fix the build configuration (e.g., `setup.py` or equivalent) so it links correctly. Fix the source code to change the pseudocount to `0.01`. Then, compile and install the package into your system Python environment.
2. **Write the Analysis Script**: Create a Python script at `/home/user/analyze_motif.py`. This script must:
   - Accept exactly one command-line argument: a DNA sequence string (composed of A, C, G, T).
   - Import the `seqmotif` package.
   - Initialize the `seqmotif.MCMCSampler()` class.
   - Call the `.fit_predict(sequence)` method, which runs the MCMC posterior estimation and returns a list of float values (the posterior probabilities of a motif starting at each position).
   - Print the exact string to standard output: `Posterior: <val1>,<val2>,<val3>,...` where each value is formatted to exactly 4 decimal places (e.g., `0.1234`). Do not print any other text.

The automated verification system will run your script with various randomly generated DNA sequences and compare its standard output bit-for-bit against a verified oracle. Your script must handle sequences of length 20 to 100 perfectly.

All work must be completed in `/home/user`.