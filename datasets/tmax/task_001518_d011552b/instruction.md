You are acting as a data scientist working on cleaning a dataset of text snippets. We have a proprietary text embedding model, but we only have access to it as a compiled, stripped Linux binary located at `/app/embedder`. 

Your goal is to write a Go program that cleans a noisy dataset using embedding-based anomaly detection, and then computes the centroid of the clean data.

Here are the specific requirements:
1. **Data Ingestion**: Read the CSV file at `/app/dataset.csv`. It contains two columns: `id` and `text`. There are 500 records.
2. **Embedding Computation**: For each `text` entry, execute the binary `/app/embedder <text>`. The binary will print a 16-dimensional embedding as comma-separated floats to standard output. Parse these into float slices in your Go code.
3. **Similarity Search & Anomaly Detection**: For every record, compute its Euclidean distance to all other records. Find its 5th nearest neighbor (where the 1st nearest neighbor is the record itself, distance 0). 
4. **Dataset Cleaning**: If a record's distance to its 5th nearest neighbor is strictly greater than `2.5`, consider it an anomaly/noise and remove it from the dataset.
5. **Centroid Calculation**: Compute the mean vector (centroid) of the remaining (clean) records.
6. **Output**: Save the 16-dimensional centroid as a single line of comma-separated floats to `/app/output_centroid.txt`.

You must implement the solution in Go. You can create your Go project in `/home/user/cleaner`.

Make sure your final output is accurate. We will evaluate your result by calculating the Mean Squared Error (MSE) between your centroid and the mathematically correct centroid of the clean dataset.