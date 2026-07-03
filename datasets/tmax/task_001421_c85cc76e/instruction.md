You are acting as a bioinformatics software engineer. We have a multi-service pipeline for processing short DNA sequences, and we need you to build the analytical core and expose it as a web service.

The environment relies on two existing services:
1. A Redis database (runs on `127.0.0.1:6379`).
2. A Mock Sequencer API (runs on `127.0.0.1:8001`).

You need to create a new Python web service (using Flask or FastAPI) that runs on `127.0.0.1:8080`. Your service must expose a single HTTP GET endpoint: `/api/v1/network-stats`.

When a GET request is made to `/api/v1/network-stats`, your service must perform the following workflow:

1. **Data Ingestion & Caching**:
   - Fetch the JSON list of DNA sequences from `http://127.0.0.1:8001/api/reads`.
   - Store the fetched JSON array as a serialized string in Redis under the exact key `dna_raw_reads`.

2. **Graph Construction** (Graph Algorithms):
   - Treat each sequence in the list as a node in an undirected graph. The nodes should be identified by their integer index in the list (0 to N-1).
   - An edge exists between Node `i` and Node `j` (where `i != j`) if and only if they share at least one exact contiguous matching $k$-mer of length $k=4$. (For example, "ATGC" in "AATGC" and "ATGCC").
   - You must build this undirected graph. We recommend using the `networkx` library.

3. **Curve Fitting**:
   - Calculate the degree of every node in the graph.
   - Sort the degrees in descending order. Let this sorted array be $Y$.
   - Let $X$ be the corresponding zero-based indices (0, 1, 2, ..., N-1).
   - Use `scipy.stats.linregress` to fit a linear model $Y = mX + c$ to these points.

4. **Response**:
   - The endpoint must return an HTTP 200 OK with a JSON payload of exactly this structure:
     ```json
     {
       "slope": <float>,
       "intercept": <float>,
       "max_degree": <int>
     }
     ```
   - Float values should be rounded to 4 decimal places.

**Setup Instructions:**
- The existing services are located in `/home/user/app/`. You will find a `start_services.sh` script there. Execute this script in the background to start Redis and the Mock API before testing your service.
- You are responsible for creating your Python service script (e.g., `/home/user/app/agent_service.py`) and starting it. You will need to install any required packages (like `flask`, `redis`, `networkx`, `scipy`, etc.) into a virtual environment or directly.

Ensure your service is left running on port 8080 so the automated verification system can issue HTTP requests against it.