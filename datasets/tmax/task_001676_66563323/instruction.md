You are a machine learning engineer preparing training data based on molecular graph topological features. You need to extract a molecular structure from an image, simulate random walks on it to compute structural features, compare the results against a reference dataset, and serve the final metrics via an API.

Follow these steps:
1. **Extract Molecular Graph:** You are given an image at `/app/molecule_data.png` containing a text representation of a molecular graph's edges. Use `tesseract` (which is preinstalled) to extract this text. The text contains lines with pairs of space-separated node IDs representing undirected edges.
2. **Monte Carlo Simulation in C:** Write a C program (`/home/user/simulate.c`) that reads these edges and simulates 1,000,000 random walks. Each walk starts at node 0 and moves to a uniformly chosen random neighbor until it returns to node 0. Calculate the average number of steps required to return to node 0.
3. **Reference Comparison:** Compare your simulated average return time for node 0 with the theoretical value provided in `/app/reference.csv`. Calculate the absolute error between your simulated value and the reference value.
4. **Data Visualization:** Generate a plot (e.g., using Python and matplotlib, or gnuplot) showing the distribution of return times for the first 1,000 random walks. Save this plot as `/home/user/return_distribution.png`.
5. **Serve Metrics:** Create and start an HTTP server (you may use Python for this part) listening on `0.0.0.0:8080`. It must expose a `GET /stats` endpoint that returns a JSON object with two keys:
   - `"average_return_time"`: Your simulated average return time (float).
   - `"error"`: The absolute difference between your simulation and the reference value (float).

Ensure your server is running in the background and accessible.