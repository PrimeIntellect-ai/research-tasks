You are a data scientist debugging a C++ embedding pipeline. 

We have a C++ script at `/home/user/embed_pipeline.cpp` that reads a dataset of items (`/home/user/raw_items.csv`), performs a basic random projection (a simple dimensionality reduction technique) to compute 3D embeddings, and is supposed to output them. 

However, similar to a plotting script that outputs blank images due to bad data, our C++ pipeline is producing severely distorted or NaN embeddings. This is because the raw dataset contains missing values (encoded as `-999.0`) and extreme outliers, which completely warp the dimensionality reduction projection matrix.

Your task is to fix the pipeline and find the most similar items:
1. Modify `/home/user/embed_pipeline.cpp` to implement data cleaning **before** the projection step.
2. For each column, calculate the mean and standard deviation of the valid values (ignore `-999.0` when computing these statistics).
3. Impute any missing values (`-999.0`) with the computed column mean.
4. Cap (clip) any outliers to be within 3 standard deviations of the mean (i.e., if a value is > mean + 3*std, set it to mean + 3*std; if < mean - 3*std, set it to mean - 3*std).
5. Ensure the C++ script outputs the cleaned, projected embeddings to `/home/user/clean_embeddings.csv`.
6. Once the embeddings are fixed, find the top 3 most similar items (closest in Euclidean distance) to the item at row index `0` (excluding item `0` itself) based on the new 3D embeddings.
7. Write the 0-based row indices of these top 3 items as a single comma-separated line to `/home/user/top3_similar.txt` (e.g., `4,7,12`).

You must write your data cleaning and similarity logic in C++. You can use standard libraries. Compile your fixed code using `g++ -std=c++11 embed_pipeline.cpp -o embed_pipeline` and run it to produce the required output.