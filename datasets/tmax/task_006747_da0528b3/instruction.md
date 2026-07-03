You are an ML engineer preparing training data. We have a large set of embeddings that need dimensionality reduction before they can be stored in our production database. 

There is a dataset of 50-dimensional float vectors located at `/home/user/data/embeddings.csv` (no header, 1000 rows).

Your task is to write and execute a Rust program to reduce the dimensionality of this dataset and log the experiment.

1. Create a new Rust project named `dim_reducer` in `/home/user/project`.
2. Write a Rust program that uses the `linfa` and `linfa-pca` crates (along with `ndarray` and `csv`) to:
   - Read the 50-dimensional vectors from `/home/user/data/embeddings.csv` into a 2D array.
   - Fit a PCA model and reduce the dimensionality to exactly 5 components.
   - Validate the output model: ensure the resulting dataset has exactly 1000 rows and 5 columns, and contains no NaN values.
   - Save the transformed 5-dimensional vectors to `/home/user/data/reduced.csv` (comma-separated, no headers).
   - Track the experiment by writing a JSON file to `/home/user/experiment_log.json` with the exact following content structure:
     `{"input_dim": 50, "output_dim": 5, "status": "success"}`

Make sure to run your Rust program so that `/home/user/data/reduced.csv` and `/home/user/experiment_log.json` are generated successfully.