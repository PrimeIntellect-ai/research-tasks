You are a bioinformatics analyst tasked with analyzing the period-3 periodicity of a DNA sequence, a known indicator of protein-coding regions.

Your task is to build a reproducible sequence analysis pipeline.

**Inputs:**
A FASTA file is located at `/home/user/input/genome.fasta`.

**Requirements:**
1. Write a Python script (or notebook) that reads the DNA sequence from `/home/user/input/genome.fasta` (ignoring the header).
2. Map the DNA characters to a numerical indicator sequence where 'C' and 'G' are `1`, and 'A' and 'T' are `0`.
3. Perform domain decomposition: divide the sequence into contiguous, non-overlapping chunks (windows) of exactly `1200` bases. Discard any trailing bases that do not form a complete 1200-base chunk.
4. For each chunk, compute the power spectrum using the Fast Fourier Transform (FFT). The power is defined as the absolute square of the FFT complex values ($|X[k]|^2$).
5. Extract the power at the frequency index that exactly corresponds to a period of 3. (Hint: For a chunk of length $N=1200$, find the correct index $k$ representing $f = 1/3$).
6. Save the results to `/home/user/output/spectral_analysis.csv`. The CSV must have exactly two columns: `chunk_id` (integer, starting at 0 for the first chunk) and `period_3_power` (float, rounded to exactly 2 decimal places).
7. Create a simple plot of `period_3_power` vs `chunk_id` and save it to `/home/user/output/spectral_plot.png`.
8. Write a master shell script `/home/user/run_pipeline.sh` that, when executed, runs your entire analysis pipeline and produces the output files.

Ensure your code is clean, handles basic FASTA parsing, and performs the spectral analysis mathematically correctly.