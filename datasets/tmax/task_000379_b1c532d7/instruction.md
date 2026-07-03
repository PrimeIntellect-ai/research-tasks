You are tasked with processing a dataset of text snippets, reducing their dimensionality for visualization, and deploying a simple model serving endpoint.

You have been provided with a compiled, stripped binary at `/app/query_embedder`. This binary reads a single line of text from standard input and prints a 64-dimensional embedding (comma-separated floats) to standard output. 

Your goals are:
1. **Compute Embeddings**: Read `/home/user/data.csv` (which has two columns: `id` and `text`, with a header row). For each row, pass the `text` to `/app/query_embedder` to get the 64-dimensional vector.
2. **Dimensionality Reduction**: Reduce these 64-dimensional vectors to 2 dimensions using PCA. You may write a short Python script using `scikit-learn` for this step. Save the output to `/home/user/reduced.csv` with the header `id,pca1,pca2` and the corresponding reduced values for each row.
3. **Experiment Tracking**: Append a line to `/home/user/experiment.log` with the exact format `Run complete: N records processed` (where N is the number of data rows in `data.csv`, excluding the header).
4. **Model Serving**: Create a bash script at `/home/user/serve.sh` that starts a TCP server on port `8888` (listening on all interfaces, i.e., `0.0.0.0`). When a client connects and sends a single line of text via TCP, the server should pass that text to `/app/query_embedder` and send the resulting 64-dimensional embedding back to the client before closing the connection. Ensure this server can handle multiple sequential connections. Run this server in the background so it is active.

Make sure your server is running and listening on port 8888 before you finish.