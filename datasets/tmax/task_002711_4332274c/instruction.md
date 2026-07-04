I need you to build a product similarity API in Go. 

As a data analyst, I've received two messy CSV files containing product data: `/home/user/products.csv` and `/home/user/prices.csv`. 
1. Clean the data: join the two datasets on the `product_id` column. Remove any rows where the `price` is missing or negative (outliers/errors), and remove rows where the `description` is empty.
2. We have a proprietary text embedding model provided as a stripped binary located at `/app/embedder`. This binary takes a single string argument and outputs a 64-dimensional float vector as comma-separated values to stdout.
3. Compute the embeddings for all the cleaned product descriptions.
4. Build an HTTP server in Go that listens on port `8080`.
5. The server must expose an endpoint `POST /search`. The request will have a JSON body `{"query": "some text", "k": 3}`.
6. When a request is received, use the `/app/embedder` binary to get the embedding for the query, compute the cosine similarity against all products in the cleaned dataset, and return the top `k` most similar products as a JSON array of objects: `[{"product_id": "...", "score": 0.95}, ...]`.
7. Also, create a script `/home/user/benchmark.sh` that uses a tool like `hey` or `ab` to benchmark your `/search` endpoint with 100 requests and saves the output to `/home/user/benchmark_results.txt`.

Please write the Go server code to `/home/user/server.go`, start the server in the background, and run your benchmark script.