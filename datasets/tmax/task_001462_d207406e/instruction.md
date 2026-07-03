You are acting as a bioinformatics analyst tasked with building a robust, parallelized sequence analysis pipeline. We are looking for hidden periodicities in DNA sequences using spectral analysis, a technique often used to identify protein-coding regions.

Your task is to create a complete Python pipeline that processes genomic data, computes Fourier transforms in parallel, visualizes the results, and includes a test suite.

**System Constraints & Setup:**
- You do not have root access. Install any needed Python packages (like `numpy`, `matplotlib`, `pytest`, `biopython`) in user space using `pip install --user`.
- The input data is located at `/home/user/data/sequences.fasta`. (Assume this file and directory exist; do not modify the input file).
- All outputs must be saved to the directory `/home/user/output/`. You must create this directory.

**Pipeline Requirements:**
1. **Script Creation**: Write a main pipeline script at `/home/user/pipeline.py`.
2. **Data Reshaping**: Read the FASTA file. Convert each DNA sequence into a numerical array using the following strict mapping:
   - `A` = 0.25
   - `C` = 0.50
   - `G` = 0.75
   - `T` = 1.00
3. **Signal Processing**: Apply a discrete Fourier transform (FFT) to the numerical array of each sequence. Compute the Power Spectrum, defined as the square of the absolute value of the FFT coefficients ($|X[k]|^2$). 
4. **Analysis**: For each sequence, identify the frequency index `k` that has the maximum power. **Crucially, you must ignore the DC component (index k=0)** when finding the maximum.
5. **Parallel Computing**: You must process the sequences in parallel using Python's `multiprocessing` module (e.g., `multiprocessing.Pool`).
6. **Results Output**: Save the results to a CSV file at `/home/user/output/results.csv`. The CSV must have exactly this header: `SequenceID,MaxPowerIndex,MaxPowerValue`. Sort the rows alphabetically by `SequenceID`. Round the `MaxPowerValue` to 4 decimal places.
7. **Visualization**: Identify the sequence that yielded the highest overall `MaxPowerValue` across the entire dataset. Plot its Power Spectrum (Power vs. Frequency Index) and save the plot as a PNG image at `/home/user/output/top_spectrum.png`.
8. **Testing**: Write a `pytest` test suite at `/home/user/test_pipeline.py`. It must include at least one test that directly imports your reshaping and FFT logic, processes the short sequence `"ACGT"`, and asserts that the resulting length of the FFT output is exactly 4. 

To complete the task, execute your pipeline script so that the output files are generated, and then run `pytest /home/user/test_pipeline.py` to prove your code passes its own tests.