You are acting as a bioinformatics analyst. We are updating our sequence processing pipeline and need to deprecate an old legacy tool that calculates cumulative evolutionary divergence from a series of instantaneous mutation rates.

The old tool is located at `/app/divergence_scorer`. It is a stripped ELF binary.
Here is what we know about it:
- It reads a space-separated list of float64 mutation rates from standard input.
- It outputs the cumulative divergence as a single float64 formatted to 6 decimal places (e.g., `12.345678`).
- It uses a custom numerical integration algorithm similar to the trapezoidal rule, but it has a known divergence bug: due to a wrong step-size adaptation, the time interval ($\Delta t$) between measurements is completely flawed. It starts at $\Delta t = 1.0$ for the first interval, but erroneously multiplies by exactly 1.5 for each subsequent step.

Your task is to write a Go program at `/home/user/scorer.go` that perfectly replicates the behavior (and the specific step-size bug) of the legacy `/app/divergence_scorer` binary. 

Your Go program must:
1. Accept an arbitrary number of space-separated float64 values from `stdin`.
2. Compute the exact same output as the binary.
3. Print the formatted result to `stdout`.

Since we will be running automated tests that fuzz your Go script against the legacy binary with thousands of random float sequences, your implementation must be bit-exact in its equivalence.