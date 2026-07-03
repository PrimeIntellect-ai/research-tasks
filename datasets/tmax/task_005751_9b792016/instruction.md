You are an MLOps engineer tasked with recovering lost experiment lineage. Due to a tracking server failure, we have a set of raw evaluation datasets and a set of orphaned model artifact embeddings, but we don't know which data corresponds to which artifact. 

Fortunately, we know the exact feature engineering steps and the lightweight projection model architecture that was used to generate the embeddings. You need to write a Rust program to reconstruct this pipeline, run inference on the raw features, and perform a similarity search to match each data point to its corresponding orphaned artifact.

**Data sources:**
1. `/home/user/experiments/raw_features.csv` - Contains the raw input features. Headers: `id,f1,f2,f3,f4` (all features are floats, `id` is a string).
2. `/home/user/experiments/target_embeddings.json` - A JSON file mapping artifact IDs (strings) to their 2D embedding vectors (arrays of two floats).

**Pipeline to reconstruct:**
1. **Feature Engineering:** For each row, compute two derived features:
   - `feat_a = f1 + f2`
   - `feat_b = f3 * f4`
2. **Model Inference:** The model is a hardcoded linear projection. Compute the 2D output embedding `[embed_0, embed_1]` as follows:
   - `embed_0 = (feat_a * 0.5) + (f1 * 0.2)`
   - `embed_1 = (feat_b * 0.3) - (f4 * 0.1)`
3. **Similarity Search:** For each generated embedding, compute the Euclidean distance against all embeddings in `target_embeddings.json`. Find the artifact ID that is closest (has the minimum Euclidean distance) to the generated embedding.

**Your task:**
1. Initialize a new Rust project in `/home/user/tracker` (e.g., using `cargo new`).
2. Implement the pipeline described above. You may use standard crates like `csv` and `serde_json` (be sure to add them to your `Cargo.toml`).
3. Output the matches as a JSON array to `/home/user/experiments/recovered_lineage.json`. The output must be formatted exactly like this:
```json
[
  {
    "id": "data_1",
    "artifact_id": "artifact_alpha"
  },
  {
    "id": "data_2",
    "artifact_id": "artifact_beta"
  }
]
```
(The order of the JSON array elements should match the order of the rows in the CSV).

Run your Rust program so that `/home/user/experiments/recovered_lineage.json` is generated.