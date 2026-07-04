You are assisting a researcher who is organizing and benchmarking a dataset of vector embeddings for similarity search and classification.

The researcher has written a custom C program located at `/home/user/workspace/knn_pipeline.c`. This program reads a dataset of embeddings (`/home/user/workspace/dataset.csv`), normalizes the features (Z-score scaling), splits the data into a training set and a testing set, and evaluates a custom K-Nearest Neighbors (KNN) classifier. It also benchmarks the inference performance.

However, the researcher noticed that the test accuracy is suspiciously high. They suspect a classic "data leakage" bug: the feature normalization calculates the mean and standard deviation across the *entire* dataset (train + test) before splitting, instead of calculating these statistics exclusively on the training set.

Your tasks are:
1. Identify and fix the data leakage bug in `/home/user/workspace/knn_pipeline.c`. The normalization statistics (mean and standard deviation) must be computed *only* using the training data (the first `train_size` rows), but these statistics must then be used to normalize *both* the training and testing data.
2. Compile the fixed program to an executable named `/home/user/workspace/knn_pipeline_fixed` (use `gcc -O3 -lm`).
3. Run the compiled executable. It will print the corrected test accuracy.
4. Create a JSON report at `/home/user/results/report.json` with the following exact structure:
```json
{
  "leakage_fixed": true,
  "corrected_test_accuracy": <float_value_from_output>
}
```

Ensure the output accuracy in the JSON precisely matches the console output of your fixed program (up to 4 decimal places).