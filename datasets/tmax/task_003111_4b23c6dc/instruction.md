You are a bioinformatics analyst working with a proprietary sequence analysis algorithm. Your team has a legacy C binary located at `/app/seq_oracle` that computes a "spectral volatility score" for DNA sequences. 

The tool implements a specific algorithm:
1. Maps each nucleotide (A, C, G, T) to a specific floating-point weight.
2. Computes the standard discrete Fourier transform (DFT/FFT) of this numerical sequence.
3. Computes the power spectrum (squared magnitude of the complex Fourier coefficients).
4. Calculates the total variation (the sum of absolute differences between consecutive frequency bins) of the power spectrum, starting from bin 0 up to N-1.

Unfortunately, `/app/seq_oracle` has a critical memory bug: it segfaults if the input sequence is longer than 32 characters. 

We recently received a batch of long sequences in `/home/user/sequences.txt` (one sequence per line, each length 100). We need you to process these sequences.

Your task:
1. Reverse engineer the numerical mapping and exact math used by `/app/seq_oracle`. You can feed it short sequences (length <= 32) via the command line (e.g., `/app/seq_oracle ACGT`) or inspect the binary directly to figure out the constants and operations.
2. Write a fast Rust program in `/home/user/analyzer/` that accurately reproduces the algorithm of the oracle.
3. Run your Rust program on `/home/user/sequences.txt` and save the scores to `/home/user/output.txt`.

Requirements:
- Your output must be a single file `/home/user/output.txt` containing one floating-point score per line, corresponding to the sequence on the same line in `sequences.txt`.
- You can create a new Rust project using `cargo` and add standard math crates like `rustfft`.
- The automated verifier will compute the Mean Squared Error (MSE) between your `output.txt` and the true values. Your solution is accepted if the MSE is less than `1e-4`.