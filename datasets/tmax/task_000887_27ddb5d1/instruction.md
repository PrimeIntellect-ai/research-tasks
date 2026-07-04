You are a bioinformatics analyst tasked with modernizing a legacy sequence processing pipeline. We have an old, undocumented scoring tool compiled as a stripped binary located at `/app/seq_evaluator`. It calculates a "structural stability metric" for DNA sequences using numerical integration over local thermodynamic energy profiles.

Your goal is to completely reverse-engineer this binary and rewrite it in Go, ensuring bit-exact identical output.

Here is your workflow:
1. **Exploratory Analysis**: Use Monte Carlo simulation to generate a large set of random DNA sequences (strings of A, C, G, T). Save these generated sequences into an HDF5 file at `/home/user/samples.h5`.
2. **Probing**: Run the stripped binary on your generated sequences to observe its output. Document your reverse-engineering process, findings, and the deduced mathematical model (integration method, weights for A/C/G/T) in a Jupyter Notebook at `/home/user/analysis.ipynb`.
3. **Re-implementation**: Write a Go program at `/home/user/evaluator.go` that takes a single DNA sequence string as its first command-line argument and prints ONLY the computed floating-point score to standard output (matching the binary's precision exactly). 

To successfully complete the task, your Go program must serve as a drop-in replacement for the binary. We will test it by fuzzing both your Go program and the original binary with thousands of random sequences and asserting that the standard outputs are perfectly identical.

The binary is invoked as: `/app/seq_evaluator <SEQUENCE>`
Your program will be invoked as: `go run /home/user/evaluator.go <SEQUENCE>`