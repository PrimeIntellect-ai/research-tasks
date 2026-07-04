You are a performance engineer profiling and optimizing a scientific Monte Carlo bootstrap simulation tool. The lead researcher left a voice memo at `/app/secret_prior.wav` containing the critical threshold value (a single spoken integer) for the posterior estimation.

Your task is to:
1. Process and transcribe the audio file `/app/secret_prior.wav` to discover the threshold value $M$. You may use standard tools like `ffmpeg` or install transcription tools to recover the spoken number.
2. Write a highly optimized C++ program located at `/home/user/mc_estimator.cpp` and compile it to an executable at `/home/user/mc_estimator`.
3. The program must read an arbitrary number of double-precision floating-point numbers from standard input (separated by whitespace) until EOF. Let this sequence be $X$ and its length be $N$.
4. Perform exactly 10,000 bootstrap resamples of $X$. Each resample consists of $N$ draws with replacement from $X$.
5. To pass our strict scientific code regression testing, you must use a specific deterministic Pseudo-Random Number Generator. Initialize `uint64_t seed = 12345;`.
For every single draw (totaling $10,000 \times N$ draws), update the seed exactly as follows before picking the element:
`seed = (1103515245 * seed + 12345) & 0x7FFFFFFF;`
The index in the array $X$ (0-indexed) chosen for this draw is `seed % N`.
*(Note: The outer loop should iterate over the 10,000 resamples, and the inner loop should iterate over the $N$ draws).*
6. For each of the 10,000 resamples, calculate the arithmetic mean of the drawn values. 
7. Keep a running count of how many of these resamples have a mean strictly greater than $M$ (the threshold extracted from the audio).
8. Print ONLY this final integer count to standard output, followed by a newline.

Your code must be numerically stable and performant. Once you have built `/home/user/mc_estimator`, an automated adversarial fuzzer will feed it random sequences of floats and compare its output bit-for-bit against a hidden oracle.