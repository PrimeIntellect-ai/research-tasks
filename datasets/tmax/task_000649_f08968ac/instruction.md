I am a bioinformatics researcher running a genomic simulation project in `/home/user/dna_sim`. The simulation performs spectral analysis on DNA sequences to calculate a "spectral energy score", but I am dealing with non-reproducible results. 

Here is what you need to do:

1. **Observational Data Reshaping & Primer Alignment**: 
   I have a raw dataset of sequencing reads in `/home/user/dna_sim/raw_reads.dat`. The file format is interleaved: one line is the Read ID (e.g., `>Read_1`), and the next line is the sequence. 
   Process this file to extract ONLY the sequences that begin exactly with the primer motif `GATTACA`. Extract just the sequence strings (no IDs) and save them to `/home/user/dna_sim/filtered_reads.txt`, with one sequence per line.

2. **Fixing the Spectral Simulation**:
   I have a C program at `/home/user/dna_sim/sim.c` that reads `filtered_reads.txt`. For each sequence, it maps the nucleotides to numerical values (A=1.0, C=-1.0, G=0.5, T=-0.5), computes a 1D Fast Fourier Transform (FFT) using FFTW3, and calculates the total spectral energy.
   
   However, because of the OpenMP parallel reduction loop at the end of the spectral calculation, the floating-point addition order varies between runs. This non-reproducibility causes the final energies to fluctuate, and they fail to match my trusted ground truth `/home/user/dna_sim/reference.txt`.

   You must fix `sim.c` to enforce strict reproducibility and minimize floating-point round-off error:
   - Remove the non-deterministic `#pragma omp parallel for reduction` used for the summation.
   - For each sequence, store the calculated energy of each frequency bin `(real^2 + imag^2)` into an array of `double`s.
   - **Sort** this array of energies in ascending order (you can use `qsort`).
   - Sequentially sum the sorted array using a standard `for` loop to compute the `total_energy`.
   
   *Note: You may need to install the FFTW3 development libraries to compile the code.*

3. **Execution & Reference Comparison**:
   Compile your fixed C program. Ensure it produces deterministic output. Run it and redirect its standard output to `/home/user/dna_sim/final_scores.txt`.
   Compare your results against `/home/user/dna_sim/reference.txt`. If your logic is correct, the values should perfectly align with the reference dataset.

Please leave the completely correct results in `/home/user/dna_sim/final_scores.txt` (format: `Sequence_X: <score>`).