You are a data analyst tasked with processing a dataset of text excerpts using a custom linear model in C++.

You have two input files:
1. `/home/user/data.csv`: Contains two columns, `id` (integer) and `text` (string enclosed in double quotes).
2. `/home/user/weights.csv`: Contains two columns, `char` (a single lowercase letter from 'a' to 'z') and `weight` (a floating-point number representing the model weight for that character).

Your task is to write and execute a C++ program that builds an ETL pipeline to process this data, compute character embeddings, perform model inference, and output classifications. 

Specifically, your C++ program must:
1. Read `/home/user/data.csv`.
2. For the `text` in each row, compute a 26-dimensional "character embedding". This embedding is the frequency distribution of the letters 'a' through 'z' (case-insensitive). Ignore any non-alphabetic characters. Normalize the vector so that the sum of the counts equals 1.0. If a text contains no alphabetic characters, the embedding should be a vector of exactly 26 zeros.
3. Read `/home/user/weights.csv` to reconstruct the linear model weights.
4. Perform inference by calculating the dot product between the text's 26-dimensional character embedding and the model weights.
5. Classify the text: if the resulting score is greater than 0.25, the prediction is `1`, otherwise `0`.
6. Write the results to `/home/user/predictions.csv` with the exact header `id,score,prediction`. The `score` must be formatted to exactly 4 decimal places (e.g., `0.1234`).

You may use standard C++ libraries (e.g., `<iostream>`, `<fstream>`, `<vector>`, `<string>`, `<iomanip>`). Compile your program using `g++ -O3` and run it to produce the output file.