You are a machine learning engineer tasked with preparing bioinformatics data for a downstream structural prediction model. You need to extract sequences, filter them based on a primer match, compute a distance matrix, perform matrix decomposition to extract features, and statistically test the most prominent feature against provided class labels.

All your work must be done within the `/home/user` directory.

Here are your instructions:
1. **Environment Setup**: Create a Python virtual environment at `/home/user/venv`. Install `numpy` and `scipy` within this environment. You must use this environment to run your Python scripts.
2. **Data Parsing and Filtering**: 
   - Read the DNA sequences from `/home/user/data/seqs.fasta`.
   - Filter the sequences to keep ONLY those that contain the exact primer substring `"GATCA"`. 
   - Sort the remaining filtered sequences alphabetically by their sequence ID (e.g., `seq_01`, `seq_02`).
3. **Distance Matrix**:
   - For the filtered and sorted sequences, compute a pairwise Hamming distance matrix $D$. $D_{i,j}$ is the number of mismatched characters between sequence $i$ and sequence $j$ (all sequences are guaranteed to be of the same length).
4. **Matrix Decomposition**:
   - Perform Singular Value Decomposition (SVD) on the distance matrix $D$.
   - Let $D = U \Sigma V^T$. Compute the feature matrix $X = U \Sigma$ (where $\Sigma$ is a diagonal matrix of the singular values).
   - Extract the first feature vector $f_1$, which corresponds to the first column of $X$ (associated with the largest singular value).
5. **Statistical Hypothesis Comparison**:
   - Read the binary labels (0 or 1) for each sequence from `/home/user/data/labels.csv` (Format: `seq_id,label`).
   - Using the labels for the *filtered* sequences, partition the values of $f_1$ into two groups (Group 0 and Group 1).
   - Perform a two-sided Welch's t-test (t-test for independent samples with unequal variances) comparing Group 0 and Group 1 on the feature $f_1$.
6. **Output**:
   - Save the results in a JSON file at `/home/user/output.json` with the following exact keys and types:
     - `"num_filtered_sequences"`: integer, the number of sequences after primer filtering.
     - `"max_hamming_distance"`: integer, the maximum value in the matrix $D$.
     - `"top_singular_value"`: float, the largest singular value (rounded to 4 decimal places).
     - `"t_statistic"`: float, the test statistic from the Welch's t-test (rounded to 4 decimal places).
     - `"p_value"`: float, the p-value from the Welch's t-test (rounded to 4 decimal places).

Make sure to strictly follow the output format. You may write one or more scripts to accomplish this.