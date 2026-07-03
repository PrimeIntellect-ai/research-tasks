You are acting as a Machine Learning Engineer preparing a subset of training data for a recommendation system. The dataset consists of a large number of user embeddings, but you only want to train on users who are highly similar to a specific reference persona. Additionally, you need to validate the statistical properties of this subset to ensure the features aren't overly correlated before feeding them into the model.

You have been provided with two files in your home directory:
1. `/home/user/embeddings.bin`: A flat binary file containing 50,000 dense vectors, each of dimension 10. The values are standard 32-bit floating-point numbers (`float` in C++), stored consecutively in row-major order (500,000 total floats).
2. `/home/user/ref_vector.txt`: A text file containing the 10-dimensional reference persona vector as 10 space-separated 32-bit floats.

Your task is to write a C++ program (saved as `/home/user/prepare_data.cpp`) that performs the following data processing pipeline:

**Step 1: Similarity Search**
Read the vectors from `embeddings.bin` and compute the Cosine Similarity between each vector and the reference vector from `ref_vector.txt`. Keep only the vectors that have a Cosine Similarity $\ge 0.85$.

**Step 2: Covariance Analysis (Validation)**
For the subset of vectors that passed the similarity threshold, compute the sample covariance matrix (using $N-1$ in the denominator) of their 10 dimensions. 

**Step 3: Output Reporting**
Find the maximum absolute *off-diagonal* value in the computed covariance matrix. This metric validates whether there is excessive collinearity among the features in your targeted subset.

Write the final results to a log file located at `/home/user/result_summary.txt` with exactly the following format:
```
Count: <integer_number_of_vectors_passing_threshold>
MaxCov: <maximum_absolute_off_diagonal_covariance_formatted_to_4_decimal_places>
```

Requirements:
- You must implement the solution in C++ and compile/run it in the terminal.
- Do not use external C++ machine learning or math libraries (like Eigen) that require separate installation; standard library features (`<cmath>`, `<vector>`, `<fstream>`, etc.) are sufficient and expected.
- Be careful with zero-indexing and floating-point precision (use standard `float` for reading the binary file, though you may cast to `double` for accumulation to avoid precision loss).