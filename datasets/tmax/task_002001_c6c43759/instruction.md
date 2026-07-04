You are an ML engineer preparing training data for a Graph Neural Network (GNN) model that predicts molecular binding affinities based on graph structures and sequence motifs. 

Your task consists of three parts:

1. **Fix and Install a Vendored Package**
You have been provided with a local copy of a feature extraction package located at `/app/bio-feature-extractor`. However, the package currently fails to build and install. Inspect the package, identify the compilation error (a deliberate perturbation involving strict compiler flags and an unused variable in the C extension), fix it, and install the package into your Python environment.

2. **Process the Raw Dataset**
There is a raw dataset located at `/home/user/raw_data.json`. It contains a JSON list of dictionaries. Each dictionary has:
- `id`: A unique string identifier.
- `adj`: An adjacency list representing the molecular graph (0-indexed).
- `seq`: A nucleotide sequence string.

Write a Python script to process this dataset. For each item, you must compute:
- **Spectral Gap**: Use the `compute_spectral_gap(adj_list)` function from the fixed `bio_feature_extractor` package. *Note: Ensure your data types and conversions maintain numerical stability, as the C extension expects standard Python lists.*
- **Alignment Score**: Use the `local_alignment(seq, motif)` function from the package to compute the alignment score of the sequence against the target motif: `"GATTACA"`.

3. **Serve the Features via an HTTP API**
To integrate with the ML training pipeline, build a Python web server (using Flask, FastAPI, or standard library) that serves the processed data.
- The server must listen exactly on `127.0.0.1:9090`.
- All endpoints must require an authentication header: `X-API-Key: ml-data-secret`. Return HTTP 401 if missing or incorrect.
- Implement endpoint `GET /health` which returns HTTP 200 with JSON `{"status": "ok"}`.
- Implement endpoint `GET /feature/{id}` which returns HTTP 200 with JSON:
  `{"id": "<id>", "spectral_gap": <float>, "alignment_score": <float>}`. If the ID is not found, return HTTP 404.

Leave the server running in the background or foreground so it can be verified by the testing suite. Ensure all dependencies you need are installed.