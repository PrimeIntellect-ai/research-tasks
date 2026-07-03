You are an application performance engineer analyzing the divergence of a numerical integrator caused by incorrect step-size adaptation.

We have a telemetry analysis algorithm that compares the empirical step-size distribution of the integrator to an ideal exponential distribution. However, the original parameters for this algorithm were lost, except for an old voice memo left by the senior engineer at `/app/telemetry_instructions.wav`.

Your task is to:
1. Transcribe the audio file `/app/telemetry_instructions.wav` to recover the algorithm's parameters (number of bins, range, and smoothing factor).
2. Write a Rust program that reads a single line of comma-separated floating-point numbers from standard input. These represent the integrator's step sizes.
3. Compute a histogram of these values according to the parameters recovered from the audio. Values exactly on the upper boundary of a bin go to the next bin, except for the very last bin. Ignore values outside the total range.
4. Apply the smoothing factor described in the audio to the bin counts.
5. Fit a simple linear regression $y = mx + c$ to the data, where $x$ is the center of each bin and $y$ is the natural logarithm of the smoothed bin count. Use ordinary least squares.
6. Calculate the modeled counts for each bin using the regression results: $M_i = \exp(m \cdot x_i + c)$.
7. Convert both the smoothed empirical counts and the modeled counts into probability distributions ($P$ and $Q$, respectively) by dividing by their respective sums.
8. Compute the Kullback-Leibler (KL) divergence from $Q$ to $P$, defined as $\sum P_i \ln(P_i / Q_i)$.
9. Print ONLY the final KL divergence to stdout, formatted to exactly 6 decimal places (e.g., `0.015230`).

Compile your Rust program to an executable at `/home/user/analyzer`.

Note: You may use standard Unix tools (like `ffmpeg`, `whisper`, etc., which you can install) to process the audio file. Standard Rust crates like `std` are sufficient for the math, but you may use `cargo` to manage dependencies if you wish. Ensure your executable reads from stdin and prints the result to stdout.