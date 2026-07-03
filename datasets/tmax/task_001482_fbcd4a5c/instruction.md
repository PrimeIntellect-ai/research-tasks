You are assisting a researcher who is organizing and analyzing a dataset of numerical profiles. The researcher needs a high-performance Bash pipeline to clean the data, generate embeddings using a proprietary black-box model, and perform similarity search.

The dataset is located at `/home/user/profiles.csv` and contains 1000 rows of comma-separated numerical features. Some values are missing (represented by consecutive commas, e.g., `1.2,,3.4`).

There is a stripped binary located at `/app/user_embedder`. This binary reads space-separated numerical features from standard input (one profile per line) and outputs a space-separated 5-dimensional embedding vector to standard output.

Your task is to write a Bash script at `/home/user/pipeline.sh` that performs the following steps:
1. **Data Cleaning**: Read `/home/user/profiles.csv`, and replace any missing values with `0.0`. Convert the CSV format to space-separated values.
2. **Model Inference**: Pass the cleaned data to `/app/user_embedder` to obtain the 5-dimensional embeddings. Note that the binary might be slow if invoked once per line; you should pass all lines to a single invocation or batch them efficiently.
3. **Similarity Search**: Using `awk` or pure Bash (do not use Python, R, or other languages), compute the Euclidean distance between all unique pairs of embeddings. 
4. **Output**: Find the 10 pairs of distinct rows with the smallest Euclidean distance. Output them to `/home/user/top10.txt`. 
   Format each line as: `RowA RowB Distance` (where RowA < RowB, and row indices are 1-based corresponding to the original `profiles.csv`). Sort the output by Distance in ascending order. If distances are equal, sort by RowA, then RowB.

Ensure your script is executable (`chmod +x /home/user/pipeline.sh`). The automated test will execute your script and compare your calculated distances against the ground-truth pairwise distances. Your pipeline's accuracy will be graded based on the Mean Squared Error (MSE) of the output distances for the top 10 pairs.