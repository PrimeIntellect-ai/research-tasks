You are a researcher organizing a massive dataset of high-dimensional embeddings. To deduplicate and cluster the records, you need to find the nearest neighbors for a subset of the data. 

We have provided a vendored version of the `annoy` package (a library for approximate nearest neighbor search) at `/app/annoy-1.17.2`. However, a previous team member accidentally broke its build configuration while debugging, making it excruciatingly slow or unable to build properly.

Your task:
1. Identify and fix the perturbation in the `annoy` package's configuration at `/app/annoy-1.17.2`. You need to ensure it compiles with high optimization (hint: look for optimization flags in its setup script).
2. Install the fixed package.
3. You are provided with a raw numpy dataset of dense embeddings at `/home/user/dataset.npy`. This array has the shape `(10000, 300)`.
4. Perform feature engineering: you must L2-normalize all 10,000 vectors in this dataset so that their L2 norms are exactly 1.0. 
5. Using the installed `annoy` package, build an Angular distance index of the normalized vectors. Use exactly 50 trees for the index to ensure high accuracy.
6. For the first 100 items in the dataset (indices 0 through 99), use the built index to find the top 10 nearest neighbors (including the item itself). Retrieve the neighbors by searching the index using the item's normalized vector.
7. Save your results in a JSON file at `/home/user/nearest_neighbors.json`. The JSON should be a dictionary where the keys are the string representation of the query indices (`"0"` to `"99"`) and the values are lists of the 10 nearest neighbor integer indices.

Ensure your entire workflow runs efficiently and that the computed neighbors are highly accurate.