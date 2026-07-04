You are tasked with cleaning a corrupted dataset of continuous sensor embeddings and reconstructing the legacy transformation model that originally generated them. 

We have a legacy tool located at `/app/sensor_encoder`. This is a stripped Linux binary that takes a 10-dimensional raw sensor vector as input (space-separated floats via command line) and outputs a 5-dimensional embedding vector. Unfortunately, our main dataset `/home/user/dataset/corrupted_embeddings.csv` contains embeddings that were further corrupted by a downstream bug, rendering them useless for our similarity search backend.

We need you to do the following:

1. **Model Reconstruction:** Treat `/app/sensor_encoder` as a black-box oracle. It implements a simple deterministic linear transformation without biases ($y = Wx$). Write a script to probe this binary, perform correlation/covariance analysis or direct algebraic extraction, and reconstruct the exact $5 \times 10$ weight matrix used by the legacy model. 
2. **Numerical Configuration:** Ensure your reconstructed matrix calculations use exact IEEE 754 single-precision (float32) arithmetic to match the legacy system's numerical accuracy.
3. **Dataset Cleaning & Similarity Search:** We have a repository of valid raw sensor vectors in `/home/user/dataset/raw_candidates.npy` (shape `[N, 10]`). Apply your reconstructed model to these candidates to generate clean embeddings. For each corrupted embedding in `/home/user/dataset/corrupted_embeddings.csv`, use cosine similarity to find the nearest valid clean embedding from your candidates.
4. **Integration:** Write your final reconstructed model as a Python script `/home/user/reconstructed_model.py`. This script must accept exactly 10 float arguments via the command line and print the 5-dimensional output vector (space-separated floats).

Your solution will be evaluated against a held-out test set of 1,000 raw vectors. We will run your `/home/user/reconstructed_model.py` and compute the Mean Squared Error (MSE) compared to the actual outputs of `/app/sensor_encoder`.