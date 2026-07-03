You are a Data Engineer managing an ETL pipeline for a recommendation system. A recent migration caused the pipeline to break, and the original code for generating item embeddings is missing. However, we have a backup of the PyTorch model weights and the input data.

Your task is to reconstruct the model architecture, run inference to generate embeddings, perform a similarity search, and ensure pipeline reproducibility.

**Context & Setup:**
The required files are located in `/home/user/etl_pipeline/`:
1. `data.csv`: Contains 100 items. The first column is `id`, and the remaining 10 columns (`f0` to `f9`) are continuous numerical features.
2. `model_weights.pth`: A PyTorch `state_dict` file.

The lost model was a simple PyTorch feed-forward network with the following architecture:
- Input layer: 10 features
- Fully connected hidden layer: 5 units
- Activation: ReLU
- Fully connected output layer: 3 units (the resulting embedding)

**Task Requirements:**
1. **Reconstruct and Load:** Write a Python script to define the PyTorch model matching the exact architecture above. Load the weights from `model_weights.pth` into this model.
2. **Deterministic Inference:** Read `data.csv`. To ensure pipeline reproducibility, **sort the data by `id` in ascending order** before processing. Convert the features to `torch.float32` tensors and run inference through the reconstructed model to get a 3-dimensional embedding for each item.
3. **Similarity Search:** Calculate the Cosine Similarity between the embedding for the item with `id=42` and the embeddings of all other items. 
4. **Output 1 (Recommendations):** Identify the top 3 most similar items to `id=42` (excluding 42 itself). Save their `id`s as a comma-separated list (e.g., `12,87,3`) ordered from most similar to least similar, in a file exactly at `/home/user/etl_pipeline/recommendations.txt`.
5. **Output 2 (Reproducibility):** Create a CSV file named `/home/user/etl_pipeline/embeddings.csv` containing the sorted `id`s and their corresponding embeddings. The columns must be exactly `id,e0,e1,e2`. Round the embedding values to exactly 4 decimal places before saving. Finally, compute the MD5 hash of this `embeddings.csv` file and save **only the 32-character MD5 hash string** to `/home/user/etl_pipeline/reproducibility.txt`.

Ensure your final output files exactly match the requested paths and formats so the automated pipeline checks can pass.