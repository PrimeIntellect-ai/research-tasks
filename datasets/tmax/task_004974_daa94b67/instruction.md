You are tasked with building a data quality filter for a pipeline that processes 3D embedding vectors extracted from sensor data. 

We have established baseline statistical parameters for these embeddings, but the original text file was lost. The only remaining record is a screenshot of the parameters located at `/app/thresholds.png`. 

Your goal is to:
1. Extract the baseline means and standard deviations for the 3 embedding dimensions from `/app/thresholds.png`. You can use standard tools like `tesseract` to read the image.
2. Write a C program that reads a CSV file containing 3 columns of floats (the 3D embeddings). For a given file, the program should compute the file's centroid (the mean of each of the 3 dimensions across all rows in the file).
3. Compute the Z-score for each of the 3 dimensions of the centroid using the baseline parameters extracted from the image: `Z_i = |Centroid_i - Baseline_Mean_i| / Baseline_Std_i`.
4. Calculate the Euclidean norm of these 3 Z-scores (the square root of the sum of their squares). 
5. The file is classified as a "clean" batch if this Z-score distance is less than or equal to 2.50. Otherwise, it is an anomalous ("evil") batch.
6. Create a bash script at `/home/user/detect.sh` that takes a single argument (the path to a CSV file). This script must use your C program to evaluate the CSV. The script must exit with code `0` if the file is "clean", and exit with code `1` if the file is "evil" (anomalous).

A set of training/test files is not provided directly, but your solution will be tested against a hidden adversarial corpus of clean and evil CSV files. 

Requirements:
- Your entry point must be exactly `/home/user/detect.sh`.
- The C program must be written from scratch, handle standard CSV parsing (comma-separated, no header), and be compiled locally by your script (or compiled once before the script runs).
- Use only standard bash tools and standard C library functions.