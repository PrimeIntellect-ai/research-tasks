You are an acoustic data scientist building a robust signal fingerprinting pipeline. You need to create a command-line tool that analyzes a raw signal's spectral properties, models its covariance via matrix decomposition, and computes a probability distance against a target distribution extracted from an audio recording.

**Step 1: Extract the Target Distribution**
There is an audio file located at `/app/target_dist.wav`. It contains a voice reading exactly 10 single-digit integers in sequence. 
1. Transcribe the audio to retrieve these 10 integers.
2. Normalize these 10 integers by dividing each by their total sum. This forms your discrete target probability distribution, $Q$ (a vector of length 10).

**Step 2: Build the Signal Analyzer**
Create an executable program at `/home/user/analyze_signal`. It can be written in any language (e.g., Python, C++, Bash invoking Python) but must be marked as executable (`chmod +x`) and handle execution directly.
The program must take exactly one command-line argument: a single string of 128 comma-separated floating-point numbers representing the input signal $x$.

For each input, your program must perform the following deterministic steps:
1. **Fourier Transform:** Compute the standard, unscaled 128-point Discrete Fourier Transform (FFT) of the input signal.
2. **Feature Extraction:** Extract the absolute magnitudes of the first 10 frequency components (indices 0 through 9). Let this 10-element vector be $M$.
3. **Matrix Construction:** Construct a $10 \times 10$ symmetric Toeplitz matrix $C$, where the entry at row $i$, column $j$ is defined as $C_{i,j} = M_{|i-j|}$ (using 0-based indexing).
4. **Decomposition:** Compute the Singular Value Decomposition (SVD) of $C$ and extract its 10 singular values.
5. **Signal Distribution:** Normalize the 10 singular values by dividing each by their total sum, forming the input probability distribution, $P$.
6. **Distance Metric:** Compute the Jensen-Shannon Divergence (JSD) between $P$ and $Q$ (the target distribution from Step 1). 
   - $JSD(P||Q) = \frac{1}{2} D_{KL}(P||M_{avg}) + \frac{1}{2} D_{KL}(Q||M_{avg})$
   - where $M_{avg} = \frac{1}{2}(P+Q)$ and $D_{KL}$ is the Kullback-Leibler divergence calculated using the natural logarithm (base $e$).

**Output Specification**
Your program must output ONLY the final JSD value to standard output, formatted to exactly 6 decimal places (e.g., `0.045123`), followed by a newline. Do not print any warnings, debug text, or additional characters.

An automated verifier will randomly generate thousands of 128-length float sequences and compare your program's output bit-for-bit against a reference implementation.