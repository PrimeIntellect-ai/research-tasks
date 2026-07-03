You are an AI assistant helping a machine learning engineer prepare a statistical dataset for a generative biology model. We need to extract statistical features from a set of raw DNA sequences and transform them using a biophysical interaction model.

Your task is to write and execute a Rust program that performs the following pipeline:

1. **Read Scientific Data (HDF5):**
   Read the input file located at `/home/user/raw_data.h5`. This file contains two datasets:
   - `sequences`: A 1D dataset of DNA sequences (stored as fixed-length ASCII strings or byte arrays).
   - `interaction_matrix`: A 4x4 matrix of 64-bit floats representing a baseline interaction model for the nucleotides A, C, G, and T.

2. **Sequence Processing & Linear Equation Solving:**
   For each sequence:
   - Calculate the normalized frequency of the nucleotides 'A', 'C', 'G', and 'T' (in that exact alphabetical order). The sum of frequencies for each sequence should be 1.0. This forms the right-hand side vector `b` (size 4).
   - Solve the linear system $A x = b$, where $A$ is the `interaction_matrix`. The solution vector `x` represents the transformed statistical feature vector for that sequence.

3. **Parallel Computing:**
   Because the real dataset will be massive, you must process the sequences in parallel. Use the Rust `rayon` crate (or a similar parallelization framework) to compute the feature vectors concurrently across multiple threads.

4. **Output Generation:**
   - Write the resulting feature vectors to a new HDF5 file at `/home/user/training_features.h5`. It must contain a single dataset named `features` with shape `(N, 4)` containing 64-bit floats, where N is the number of sequences. The order of rows must correspond to the original order of the sequences in the input file.
   - Finally, compute the mean of each of the 4 columns across all sequences in the `features` dataset. Write these 4 mean values as a comma-separated string (e.g., `0.12,0.34,0.56,0.78`) to the file `/home/user/feature_means.txt`.

Constraints & Environment:
- Use Rust as your primary language for this data pipeline.
- You can create your Rust project in `/home/user/feature_pipeline`.
- Standard dependencies like `hdf5`, `ndarray`, `ndarray-linalg`, and `rayon` are recommended. 
- Ensure your code compiles and runs successfully, producing the two output files: `/home/user/training_features.h5` and `/home/user/feature_means.txt`.