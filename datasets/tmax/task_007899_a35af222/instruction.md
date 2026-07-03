You are a data scientist working on a bioinformatics project. You need to process a dataset of DNA sequences, align them to a specific primer, and fit a simple statistical model relating sequence composition to alignment affinity. Because the dataset could grow large, you need to implement the alignment step using parallel processing.

Here is your task:

1. **Environment Setup**: 
   Create a Python virtual environment at `/home/user/venv`. Install `biopython` and `scikit-learn` in this environment.

2. **Data**: 
   You have been provided with a FASTA file containing DNA sequences at `/home/user/genomics_data/sequences.fasta`.

3. **Processing Script**:
   Write a Python script at `/home/user/process_alignments.py` that does the following:
   - Reads the `sequences.fasta` file.
   - Uses Python's `multiprocessing` module (e.g., `Pool` with 4 processes) to process the sequences in parallel.
   - For each sequence, computes its GC content (as a percentage from 0.0 to 100.0, e.g., 45.5).
   - For each sequence, performs a **local alignment** against the primer sequence `CGTAGCTAGCC` using Biopython's `PairwiseAligner`.
   - The aligner must be configured with:
     - `mode = 'local'`
     - `match_score = 2`
     - `mismatch_score = -1`
     - `open_gap_score = -2`
     - `extend_gap_score = -0.5`
   - Retrieves the maximum alignment score for each sequence.

4. **Model Fitting**:
   - Using the extracted data, fit a standard Ordinary Least Squares (OLS) Linear Regression model (using `sklearn.linear_model.LinearRegression`) to predict the `alignment_score` (y) based on the `gc_content` (X). Ensure X is a 2D array of shape `(n_samples, 1)`.

5. **Outputs**:
   Your script must generate two files:
   - `/home/user/results.csv`: A CSV file containing the results for all sequences. It must have exactly these columns (with a header row): `sequence_id,gc_content,alignment_score`. The rows can be in any order. Format the floats to 4 decimal places.
   - `/home/user/model_stats.txt`: A text file containing the linear regression model parameters, formatted exactly as follows:
     ```
     Slope: [slope_value]
     Intercept: [intercept_value]
     ```
     Round both values to exactly 4 decimal places.

Run your script using the virtual environment you created to produce the output files.