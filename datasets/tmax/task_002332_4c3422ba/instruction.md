As a bioinformatics analyst, you need to extract specific genetic sequences, compile a custom filtering tool, and run a spectral analysis pipeline to identify period-3 periodicities (often associated with protein-coding regions) using numerical optimization. 

Perform the following steps:

1. **Compilation & Filtering**:
   - You have a C source file at `/home/user/filter_seqs.c`. Compile it into an executable named `filter_seqs` in the same directory using `gcc`.
   - The tool takes two arguments: an input FASTA file and an output text file. Run it using `/home/user/raw_sequences.fasta` as input and `/home/user/filtered.txt` as output. This will extract only the valid sequences.

2. **Spectral Optimization**:
   - Write a Python script `/home/user/analyze.py` to process `/home/user/filtered.txt`.
   - The file contains comma-separated values: `SequenceName,SequenceString`. Find the sequence named `TARGET_SEQ`. Let its length be $N$ (guaranteed to be a multiple of 3).
   - We map the characters `A, C, G, T` to numerical weights $w_A, w_C, w_G, w_T$.
   - For a given set of weights, convert the sequence into a numerical array $x$ of length $N$.
   - Compute the Discrete Fourier Transform (DFT) of $x$ using `scipy.fft.fft`.
   - The period-3 spectral power is the absolute value (magnitude) of the DFT at index $k = N/3$.
   - Use `scipy.optimize.minimize` to find the optimal weights $(w_A, w_C, w_G, w_T)$ that **maximize** the period-3 spectral power.
   - Constraints on weights:
     - $w_A + w_C + w_G + w_T = 1.0$
     - $0 \le w_i \le 1.0$ for all $i$
   - Use an initial guess of `[0.25, 0.25, 0.25, 0.25]`. Use the `SLSQP` method.

3. **Output Generation**:
   - Extract the optimized weights.
   - Save a JSON file at `/home/user/spectral_results.json` containing the weights rounded to exactly 4 decimal places. The format must be exactly:
     ```json
     {
         "TARGET_SEQ": {
             "w_A": 0.1234,
             "w_C": 0.1234,
             "w_G": 0.1234,
             "w_T": 0.1234
         }
     }
     ```

Ensure all dependencies (like `scipy` and `numpy`) are installed if not already present. You have rootless access; use `pip` or virtual environments if needed.