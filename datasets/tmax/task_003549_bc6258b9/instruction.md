You are a data engineer tasked with building a reproducible ETL and recommendation pipeline. 

We have a Python prototype that performs dimensionality reduction via Singular Value Decomposition (SVD) on user-item interaction data to find similar items. Your goal is to reimplement this logic in C++ for performance, create a pipeline to tune its hyperparameters, and generate recommendations.

**Context & Constraints:**
- You do NOT have root/sudo access.
- The input data is located at `/home/user/data/matrix.txt`. It is a dense space-separated matrix of floats (50 rows representing users, 20 columns representing items).
- You must use C++ as the primary language for the mathematical processing. 
- You must use the **Eigen** C++ library for matrix operations. Since you lack root access, you should download Eigen3 locally (e.g., `wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz`) and compile against it.

**Python Prototype Logic to Reconstruct in C++:**
```python
import numpy as np

def compute_score(R, k):
    # R is the NxM input matrix.
    # Perform SVD: R = U * S * V^T
    U, S, Vt = np.linalg.svd(R, full_matrices=False)
    
    # Truncate to k components
    Uk = U[:, :k]
    Sk = np.diag(S[:k])
    Vtk = Vt[:k, :]
    
    # Reconstruct matrix
    R_hat = Uk @ Sk @ Vtk
    
    # Calculate score: RMSE + penalty
    # RMSE = sqrt( mean( (R - R_hat)^2 ) )
    rmse = np.sqrt(np.mean((R - R_hat)**2))
    return rmse + 0.1 * k

def get_similar_items(R, k, target_item_idx):
    U, S, Vt = np.linalg.svd(R, full_matrices=False)
    Vtk = Vt[:k, :]
    
    # Item embeddings are the columns of Vtk (or rows of Vtk.T)
    item_embeddings = Vtk.T
    target_emb = item_embeddings[target_item_idx]
    
    # Compute Cosine Similarity between the target item and all items
    # sim(A, B) = (A dot B) / (norm(A) * norm(B))
    norms = np.linalg.norm(item_embeddings, axis=1)
    target_norm = np.linalg.norm(target_emb)
    
    sims = (item_embeddings @ target_emb) / (norms * target_norm)
    sims[target_item_idx] = -np.inf # Exclude the item itself
    
    # Return indices of the top 3 most similar items in descending order of similarity
    return np.argsort(sims)[::-1][:3].tolist()
```

**Your Task:**
1. Write a C++ program that implements the above logic using Eigen. 
2. Write a bash script `/home/user/pipeline.sh` that orchestrates the workflow:
   - Compiles the C++ program.
   - Runs a hyperparameter sweep testing all integer values of $k$ from `1` to `15` inclusive.
   - Finds the optimal $k$ that **minimizes** the `compute_score` function.
   - Using that optimal $k$, computes the top 3 similar items for target item index `0`, and target item index `5`.
   - Outputs the final results into a JSON file strictly at `/home/user/output/result.json`.

**Output Format Requirements:**
The file `/home/user/output/result.json` must be strictly formatted as follows (example values):
```json
{
  "optimal_k": 7,
  "item_0_top_3": [12, 4, 19],
  "item_5_top_3": [1, 2, 3]
}
```

Make sure your pipeline is entirely reproducible by running `/home/user/pipeline.sh`.