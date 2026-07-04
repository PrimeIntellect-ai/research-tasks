You are an AI assistant helping a data scientist set up a reproducible pipeline for analyzing biological signals and genomic reads. 

We have two correlated datasets in `/home/user/data/`:
1. `signals.h5`: An HDF5 file containing a 2D dataset named `raw_signals` (shape: N x 512). These represent raw electrical signals.
2. `reads.fasta`: A FASTA file containing N DNA sequences.

Your task is to create a complete, reproducible workflow that extracts features from both datasets, aligns a specific primer, and fits a linear model. You must create a main shell script `/home/user/run_analysis.sh` that performs the following steps when executed:

1. **Signal Processing (Python)**: Read `signals.h5`. For each row in `raw_signals`, compute the discrete Fourier Transform (FFT). Find the index of the maximum magnitude frequency component (excluding the DC component at index 0, so search from index 1 to 255). Save these indices to `/home/user/peaks.txt` (one integer per line, in order of the rows).

2. **Primer Alignment (Multi-language)**: Write a script in a language of your choice (e.g., Perl, Ruby, or bash/awk) to process `reads.fasta`. For each sequence, find the 0-indexed starting position of the first occurrence of the primer sequence `GATTACA`. If the primer is not found in a sequence, output `-1` for that sequence. Save these positions to `/home/user/positions.txt` (one integer per line, in order of the sequences).

3. **Notebook-based Modeling**: Create a Jupyter Notebook named `/home/user/fit_model.ipynb` (using Python). The notebook should:
   - Read `/home/user/peaks.txt` and `/home/user/positions.txt`.
   - Filter out any rows where the position is `-1`.
   - Fit an ordinary least squares linear regression model using the peak frequency index as the independent variable (X) and the primer position as the dependent variable (Y).
   - Write the estimated slope of the regression line, rounded to 3 decimal places, to a file named `/home/user/slope.txt`.

4. **Orchestration**: `run_analysis.sh` must sequentially execute the feature extraction, the primer alignment, and finally execute the Jupyter notebook in place (e.g., using `jupyter nbconvert --to notebook --execute fit_model.ipynb`).

Ensure all scripts have correct permissions and paths. Do not assume any pre-existing modules other than standard scientific Python libraries (numpy, h5py, scipy, scikit-learn, statsmodels, jupyter) and standard Linux tools. Your final step should be to run `/home/user/run_analysis.sh`.