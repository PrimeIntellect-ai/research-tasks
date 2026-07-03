You are a data analyst troubleshooting a network routing issue. You have been provided with network topology data and an image containing the hostname of the destination node.

Your task is to calculate the shortest path through the network and serve the results via an HTTP server.

1. **Information Extraction**:
   - There is an image located at `/app/network_map.png`. Use an OCR tool (like `tesseract`) to extract the text from it. The image contains the name of the target destination router.
   - The starting router for your analysis is `ALPHA-1`.

2. **Database Operations & Graph Traversal**:
   - You have two CSV files in `/app/data/`:
     - `routers.csv`: `id,hostname,status`
     - `links.csv`: `source_id,target_id,latency` (edges are directed: source -> target)
   - Using `sqlite3`, import these CSV files into a new database `/app/network.db`.
   - Create appropriate indexes on the tables to optimize join and traversal operations.
   - Write a query (e.g., using a Recursive CTE) to find the shortest path (minimum total latency) from `ALPHA-1` to the target router extracted from the image.
   
3. **Data Export**:
   - Export the result of your shortest path query to a file named `/app/www/path.csv`.
   - The CSV should have exactly two columns: `path` and `total_latency`.
   - The `path` column must contain the sequence of hostnames separated by `->` (e.g., `ALPHA-1->ROUTER-X->TARGET`).

4. **Serve the Data**:
   - Start an HTTP server on port `8080` that serves the contents of the `/app/www/` directory.
   - An automated verifier will make a `GET` request to `http://127.0.0.1:8080/path.csv` to validate your output.
   - Ensure the server runs in the background or stays alive so the verifier can reach it.

Ensure all file formats strictly adhere to the requirements. Use bash and standard CLI tools (`sqlite3`, `tesseract`, `python3` for serving) to complete the task.