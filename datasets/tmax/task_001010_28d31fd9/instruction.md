You are a Machine Learning Engineer preparing a dataset of vector embeddings for a downstream clustering task. The raw data is currently stored in a large CSV file, but it needs to be cleaned, normalized, statistically verified, and stored in an efficient binary format to speed up training.

You have been provided a raw dataset at `/home/user/raw_embeddings.csv`. The file contains a header row `id,v0,v1,v2,v3,v4,v5,v6,v7` followed by 10,000 rows of data. The `id` is an integer, and `v0` through `v7` are floating-point numbers representing an 8-dimensional vector.

Your task is to build a robust C++ ETL pipeline that processes this data. Write a C++ program located at `/home/user/pipeline.cpp` that does the following:

1. **ETL & Linear Algebra:** Read the CSV file. For each row, extract the 8-dimensional vector (ignore the `id`). Compute the L2 norm (Euclidean length) of the vector. If the norm is greater than 0, normalize the vector by dividing each component by its L2 norm.
2. **Data Storage Management:** Write the normalized vectors to a flat binary file at `/home/user/processed_embeddings.bin`. The file should contain only the normalized vector components sequentially (row 1 `v0-v7`, row 2 `v0-v7`, etc.) as strictly 32-bit single-precision floats (`float` in C++) in standard little-endian format. Do not write the `id` or any headers.
3. **Hypothesis Testing:** We need to verify if the first dimension (`v0`) of the *normalized* vectors has a mean significantly different from 0. Calculate the sample mean and the 95% confidence interval for the normalized `v0` across all 10,000 rows. Use the formula: `CI = Mean ± 1.96 * (SampleStdDev / sqrt(N))`. Calculate the sample standard deviation using Bessel's correction (N-1).
4. Write these statistical findings to `/home/user/stats.txt` in exactly this format (rounded to 6 decimal places):
```
Mean: <value>
CI_Lower: <value>
CI_Upper: <value>
```

Compile your code using `g++ -O3 -std=c++17 /home/user/pipeline.cpp -o /home/user/pipeline` and run it to produce the outputs.