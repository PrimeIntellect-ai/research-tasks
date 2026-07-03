You are an ML Engineer preparing training data for a Bayesian inference model. The pipeline currently ingests a large binary dataset containing sensor readings, but there is a silent data-corruption issue. Similar to how pandas might silently convert integers to floats when introducing NaNs, our upstream data ingestion encodes missing sensor readings as exactly `-999.0f` (32-bit floats), which heavily skews our covariance calculations if not explicitly handled. 

You need to write a C program that acts as a robust data preparation and testing step. 

The raw dataset is located at `/home/user/raw_data.bin`. It contains tightly packed 32-bit `float` values representing records. Each record consists of 3 features: `X`, `Y`, and `Z`. The total number of bytes in the file is a multiple of 12 (since each record is 3 * 4 bytes).

Your task is to:
1. Write a C program named `/home/user/clean_covar.c` that reads the binary file `/home/user/raw_data.bin`.
2. Iterate through the records. If *any* feature in a record equals `-999.0f`, you must completely discard that entire record (row) from your calculations.
3. Compute the sample covariance matrix (a 3x3 matrix) for the remaining valid records. Use the standard unbiased sample covariance formula (dividing by N - 1, where N is the number of valid records).
4. The C program must output the final 3x3 covariance matrix to `/home/user/expected_covar.txt`. 

The output file `/home/user/expected_covar.txt` must format the matrix exactly as follows, with 4 decimal places:
```
Cov(X,X), Cov(X,Y), Cov(X,Z)
Cov(Y,X), Cov(Y,Y), Cov(Y,Z)
Cov(Z,X), Cov(Z,Y), Cov(Z,Z)
```
Example line format: `1.2345, 0.1234, -0.9876`

Compile your program using `gcc /home/user/clean_covar.c -o /home/user/clean_covar -lm` and run it to produce the output file.