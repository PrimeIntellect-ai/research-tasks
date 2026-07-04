You are tasked with setting up and integrating a data processing pipeline for a simulated polymer network experiment. The system consists of multiple microservices that generate, process, and serve spectroscopic and molecular graph data.

The environment in `/app/` contains the following files:
- `simulator.py`: A raw TCP daemon. When started, it listens on port 9000. Any client that connects to `127.0.0.1:9000` will receive a JSON string representing an array of 1024 float values (a time-domain signal sampled at 1024 Hz for 1 second) and the connection will be closed.
- `molecule.json`: A JSON file representing a molecular graph. It has the structure `{"nodes": [{"id": int, "base_freq": float}, ...], "edges": [[node_id, node_id], ...]}`.
- `nginx.conf`: An Nginx configuration file template. 
- `start_env.sh`: A shell script that starts the simulator and a local redis instance (port 6379), but NOT Nginx or your processor.

Your objectives:

1. **Fix the API Gateway (Nginx):** 
   Modify `/app/nginx.conf` so that Nginx listens on port `8080` (HTTP) and proxies any requests starting with `/api/` to `127.0.0.1:5000`.

2. **Implement the Spectral Graph Processor (Python):**
   Create a Flask application named `/app/processor.py` that listens on `127.0.0.1` port `5000`. It must implement two endpoints:
   
   - `GET /api/signal`
     - When called, it must establish a raw TCP connection to `127.0.0.1:9000` and read the JSON array of 1024 floats.
     - Perform a Fast Fourier Transform (FFT) on the signal to find the *dominant frequency* in Hz (the frequency index with the highest magnitude, ignoring the DC component/index 0). Assume a sampling rate of 1024 Hz.
     - Return a JSON response: `{"dominant_frequency": <int>}`.

   - `GET /api/graph/<int:freq>`
     - Read `/app/molecule.json`.
     - Identify all "resonating" nodes in the graph. A node resonates if the absolute difference between its `base_freq` and the requested `<freq>` is strictly less than `3.0`.
     - Consider the subgraph induced by ONLY these resonating nodes. Calculate the size (number of nodes) of the largest connected component within this subgraph.
     - Return a JSON response: `{"max_component_size": <int>}`.

3. **Orchestrate the Services:**
   - Run `/app/start_env.sh` to start the simulator and redis.
   - Start Nginx using your modified `/app/nginx.conf` (`nginx -c /app/nginx.conf`).
   - Start your Flask application (`python3 /app/processor.py`) in the background.

The automated verification suite will make HTTP requests directly to your Nginx gateway on port 8080 to test the entire end-to-end flow. Ensure your Flask app continues running and doesn't crash after a single request.