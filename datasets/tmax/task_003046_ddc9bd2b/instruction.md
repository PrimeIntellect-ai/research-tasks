You are acting as a machine learning engineer preparing training data and building a similarity search pipeline. We need to implement a reproducible dimensionality reduction and nearest-neighbor search utility in C.

Your task is to write a C program that reads a dataset of high-dimensional vectors, reduces their dimensionality using a deterministic random projection, and finds the closest matches for a specific query item. 

Here are the specific requirements:

1. **Input Data**: 
   A CSV file is located at `/home/user/data/vectors.csv`. The file has no header. Each line is formatted as: `id,f1,f2,f3,f4,f5` (where `id` is an integer, and `f1` to `f5` are floating-point numbers). There are exactly 100 rows.

2. **Dimensionality Reduction**:
   Write a C program that projects the 5-dimensional vectors into a 2-dimensional space. 
   - The projection matrix $M$ is a $5 \times 2$ matrix (5 rows, 2 columns).
   - To ensure reproducibility (Pipeline reproducibility testing), initialize the random number generator using `srand(seed)`, where `seed` is passed as the first command-line argument to your C program.
   - Populate the matrix in row-major order (i.e., $M[0][0], M[0][1], M[1][0], \dots, M[4][1]$).
   - For each element, generate a random float between 0.0 and 1.0 (inclusive of 0.0, strictly less than 1.0? No, let's use exact formula: `(double)(rand() % 1000) / 1000.0`).
   - The projected 2D vector $P_i$ for an original vector $V_i$ is computed as $P_i = V_i \times M$.

3. **Similarity Search**:
   - The query item has `id = 42`.
   - Calculate the Euclidean distance in the new 2D space between the projected vector of `id = 42` and the projected vectors of all other items in the dataset.
   
4. **Execution and Output**:
   - Save your C code to `/home/user/src/search.c` and compile it to `/home/user/src/search`.
   - Run your program using the random seed `2024`.
   - Find the 3 most similar items (lowest Euclidean distance) to `id = 42`, excluding the item itself.
   - If there are ties in distance, break them by selecting the smaller `id`.
   - Write the results to `/home/user/output/recommendations.txt`. The file must contain exactly 3 lines, formatted as `id,distance` with the distance rounded to 4 decimal places (e.g., `%.4f`). Ensure the output directory exists before writing to it.

You must handle the file reading, matrix multiplication, distance calculation, and sorting natively in C.