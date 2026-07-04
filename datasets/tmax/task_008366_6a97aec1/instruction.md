You are a data engineer building a high-performance ETL pipeline in C to generate recommendations. You need to write a C program that reads user features, applies a pre-trained linear projection using OpenBLAS, and matches each user to the closest item using Euclidean distance.

Your task:
1. Install the OpenBLAS development library (e.g., `libopenblas-dev`).
2. Write a C program at `/home/user/etl_recommend.c`.
3. The program must read three input files located in `/home/user/data/`:
   - `weights.csv`: A 3x5 projection matrix (3 rows, 5 columns, comma-separated double-precision floats).
   - `items.csv`: Contains item embeddings. Each line format is `ItemID,e1,e2,e3` (integer ID followed by 3 doubles).
   - `users.csv`: Contains user features. Each line format is `UserID,f1,f2,f3,f4,f5` (integer ID followed by 5 doubles).
4. **Data schema enforcement**: Your program must gracefully skip any lines in `users.csv` or `items.csv` that do not perfectly match the expected number of comma-separated columns (e.g., skip lines with missing values or invalid formats).
5. **Model inference & Similarity search**: For each valid user vector $u$ (5x1):
   - Compute the projected 3D embedding $p = W \times u$ using `cblas_dgemv` from the OpenBLAS library.
   - Find the valid item in `items.csv` that has the minimum Euclidean distance to $p$.
6. Output the results to `/home/user/recommendations.csv` in the format `UserID,RecommendedItemID`. Do not include a header. Output rows should be in the order the valid users appear in `users.csv`.
7. Compile your program to `/home/user/etl_recommend` using `gcc` and linking against OpenBLAS (`-lopenblas`) and the math library (`-lm`).
8. Run the executable to produce the output.

Ensure your program handles the matrix multiplication correctly according to BLAS row/column major formats.