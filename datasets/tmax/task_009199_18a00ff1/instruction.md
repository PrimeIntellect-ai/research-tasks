We are preparing training data for an integer-quantized machine learning model. Previously, we used a Pandas pipeline to reduce our dataset's dimensionality, but it silently converted our integer features to floats when it encountered missing values (NaNs). This type-casting causes our downstream C++ inference engine to fail validation.

Your task is to write a highly performant, reproducible C++ pipeline to replace the Pandas script. 

Write a C++ program at `/home/user/reducer.cpp` that does the following:
1. Reads `/home/user/dataset.csv`. This file contains an unknown number of rows and exactly 10 columns of integer data. Some values are missing (represented by consecutive commas, e.g., `12,,34`).
2. Imputes any missing values with the integer `0`.
3. Performs a simple deterministic dimensionality reduction: reduce the 10 columns to 5 columns by summing adjacent pairs of columns. (i.e., New Column 1 = Col 1 + Col 2; New Column 2 = Col 3 + Col 4, etc.).
4. Writes the reduced data to `/home/user/reduced.csv`. The output must be perfectly formatted as a CSV with exactly 5 columns of strictly integer values (no decimal points, e.g., `12,34,56,78,90`).
5. Tracks the inference/processing execution time (excluding program startup/initialization, but including the file I/O and processing loop) and writes the elapsed time in milliseconds (as a simple integer or float) to `/home/user/benchmark.txt`.

Compile your code to `/home/user/reducer` using `g++ -O3 -std=c++17` and execute it to generate the outputs.