You are a performance engineer optimizing a bioinformatics data analysis pipeline. The pipeline processes large sets of DNA sequences to find periodic signals using spectral analysis, but the current implementation is too slow.

Your task is to write a parallelized script in the language of your choice that reads a provided FASTA file, performs mathematical transformations and spectral analysis on the sequences, and outputs a summary.

The input data is located at: `/home/user/input/sequences.fasta`

For each sequence in the FASTA file, your script must perform the following steps:
1. Parse the sequence data (ignoring the `>` header lines but keeping track of the sequence ID, e.g., `seq_001`).
2. Convert the nucleotide characters into a numeric array using the following mapping:
   - `A` -> 1.0
   - `C` -> -1.0
   - `G` -> 2.0
   - `T` -> -2.0
3. Compute the 1-Dimensional Discrete Fourier Transform (FFT) of the numeric array.
4. Compute the Power Spectral Density (PSD), which is the absolute value squared of the FFT result (i.e., $|X[k]|^2$).
5. Calculate the "sequence energy" by numerically integrating the PSD array using the **Trapezoidal rule**. Assume a uniform spacing of `dx=1.0` between data points.

**Performance Requirement:** 
You must implement parallel computing (e.g., using `multiprocessing` in Python, OpenMP in C++, or equivalent) to distribute the processing of the sequences across at least 4 parallel workers/threads.

**Output:**
Once all sequences are processed, calculate the total energy across all sequences. Generate a JSON log file at `/home/user/summary.json` containing exactly the following keys:
- `"max_energy_id"`: A string of the ID (e.g., `"seq_042"`) of the sequence that had the highest computed energy.
- `"total_energy"`: A float representing the sum of the energies of all sequences, rounded to 1 decimal place.
- `"parallel_workers"`: An integer representing the number of parallel workers your script used (must be >= 4).

Ensure your script handles standard FASTA formatting, where sequence data may be split across multiple lines.