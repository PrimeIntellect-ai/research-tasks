As a machine learning engineer, you need to prepare a highly specific synthetic training dataset of molecular graph properties for a Graph Neural Network. The data pipeline involves generating random graphs, filtering them via Monte Carlo rejection sampling to match a target density distribution, and parallel-posting the accepted properties to an ingestion service backed by a Redis database.

**Your Objectives:**

1. **Service Configuration (Multi-Service Compose)**
   You are provided with an ingestion pipeline in `/app/`.
   - `redis-server` must run on its default port (6379).
   - `/app/ingestion.py` is a Flask application that receives POST requests at `/ingest` and stores them in Redis. It currently has configuration errors preventing it from connecting to Redis or binding to the correct local loopback interface. Fix `/app/ingestion.py` and start both services in the background.

2. **C++ Data Generator Implementation**
   Create a C++ program at `/app/generator.cpp`. This program must:
   - Generate random Erdős–Rényi undirected graphs with $N=100$ nodes. The edge probability $p$ for each generated graph should be drawn uniformly from $[0.1, 0.5]$.
   - Compute the global clustering coefficient $C$ for each generated graph (ratio of closed triplets to total connected triplets).
   - Use **Monte Carlo Rejection Sampling** to filter these graphs. We want the distribution of the accepted graphs' clustering coefficients to follow a Normal distribution with $\mu = 0.30$ and $\sigma = 0.05$. (Hint: You can use a uniform proposal bounding box over the theoretical range of $C$).
   - Use **OpenMP** to parallelize the graph generation, property calculation, and sampling loop.
   - For every *accepted* graph, immediately send an HTTP POST request to `http://127.0.0.1:8000/ingest` with the JSON payload `{"c": <value>}`. (Use `libcurl`).
   - Stop once exactly 10,000 accepted values have been successfully sent.

3. **Execution & Metric Constraints**
   - Compile your code with `g++ -O3 -fopenmp -lcurl /app/generator.cpp -o /app/generator`.
   - Run the generator.
   - The final statistical fidelity of the ingested dataset will be measured using the Kolmogorov-Smirnov (K-S) test. The $D$-statistic comparing your 10,000 ingested values against the theoretical $\mathcal{N}(0.30, 0.05^2)$ distribution must be less than `0.03`.

Ensure all code runs successfully and completes data generation. Do not write output validation scripts; the system will verify the Redis database state directly.