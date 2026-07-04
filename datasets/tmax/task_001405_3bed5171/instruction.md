I am a data analyst trying to compute the centroid (average vector) of a dataset of embedding vectors stored in a CSV file. I wrote a C program to do this because the dataset is supposed to get very large, but there's a bug: the output is just zeroes, almost like a blank plot in matplotlib but for data. 

I have placed the dataset at `/home/user/embeddings.csv`. It contains 1000 rows, each with 5 comma-separated floating-point numbers representing an embedding.
My broken C code is at `/home/user/aggregate.c`. 

Please fix my C code so that it correctly computes the column-wise mean (centroid) of the dataset. 
Requirements:
1. Fix the numerical accuracy bug in `/home/user/aggregate.c`.
2. Compile the fixed code using `gcc` to an executable named `/home/user/aggregate`.
3. Run the executable. It must read `/home/user/embeddings.csv` and write the correct centroid to `/home/user/centroid.csv`.
4. The output `/home/user/centroid.csv` must contain exactly one line with 5 comma-separated numbers, each formatted to exactly 4 decimal places (e.g., `0.1234,-0.5678,...`).

Do not change the input/output file paths in the C code.