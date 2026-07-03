You are an AI assistant helping a machine learning engineer prepare training data by filtering out highly correlated features. 

We have a dataset stored as a raw binary file at `/home/user/dataset.bin`. The file contains exactly 10,000 samples, each with 10 features. The data is stored in row-major order, and every value is a standard 64-bit IEEE 754 floating-point number (`double` in C). There is no header in the file.

Your task is to:
1. Ensure your analysis environment is set up (e.g., install `gcc` and `make` if needed).
2. Write a C program at `/home/user/cov_analyzer.c` that reads `/home/user/dataset.bin`.
3. The program must compute the Pearson correlation coefficient between all pairs of the 10 features.
4. Identify all pairs of features (0-indexed) that have an absolute Pearson correlation coefficient strictly greater than `0.85`.
5. Compile and run your program to generate an output file at `/home/user/correlated_features.txt`.

The output file `/home/user/correlated_features.txt` must contain one pair per line, formatted as `X,Y` where `X` and `Y` are the integer indices of the features, and `X < Y`. The lines should be sorted in ascending order of `X`, then `Y`.

Example of expected output format in `/home/user/correlated_features.txt`:
1,4
2,8
5,9

Do not use any external math libraries other than the standard C math library (`-lm`).