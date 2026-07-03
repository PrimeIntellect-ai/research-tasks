You are a machine learning engineer tasked with preparing a training dataset from a large-scale raw data dump. 

You have been provided with a large CSV file located at `/home/user/raw_data.csv`. This file contains 100,000 rows and 10 columns of numerical raw features (floats). Due to the size of typical datasets in our pipeline, we require a memory-efficient C++ solution to stream this data, sample it deterministically, and engineer new embedding features.

Write and execute a C++ program at `/home/user/prepare.cpp` that performs the following steps:
1. **Streaming & Sampling**: Read `/home/user/raw_data.csv` line-by-line (do not load the entire file into memory). Keep only the rows where the 0-based row index `L` satisfies the condition: `(L * 9973) % 100000 < 1000`.
2. **Feature Engineering / Embedding**: For each selected row (which has 10 feature values, $x_0$ to $x_9$), compute a new 3-dimensional embedding vector $E = [e_0, e_1, e_2]$ using polynomial feature expansion:
   - $e_0 = \sum_{j=0}^{9} x_j \cdot (j + 1)$
   - $e_1 = \sum_{j=0}^{9} x_j \cdot (j + 1)^2$
   - $e_2 = \sum_{j=0}^{9} x_j \cdot (j + 1)^3$
3. **Output**: Write the newly computed 3D embeddings to `/home/user/processed_embeddings.csv`. Each line should represent one sampled row and contain the 3 computed values separated by commas. Format the output to exactly 4 decimal places (e.g., using `std::fixed` and `std::setprecision(4)`).

Compile your C++ program using `g++ -O3 /home/user/prepare.cpp -o /home/user/prepare` and run it to produce the final `processed_embeddings.csv` file. 

The task is complete when `/home/user/processed_embeddings.csv` exists and contains the correctly formatted, sampled embeddings.