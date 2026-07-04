You are a data scientist working on cleaning a dataset of synthetic materials. The dataset contains several numerical properties, but some features might be highly redundant. 

Your task is to write a Rust program that performs correlation analysis to clean the dataset, and then implements a similarity search to recommend similar materials.

**Dataset:**
You have a CSV file located at `/home/user/materials.csv` with the following columns:
`id`, `density`, `tensile_strength`, `flexibility`, `thermal_conductivity`, `electrical_conductivity`.

**Requirements:**
1. **Initialize a Rust Project:** Create a new Cargo project in `/home/user/material_cleaner`. You may use crates like `csv`, `serde`, `serde_json`, or `ndarray` by adding them to your `Cargo.toml`.
2. **Correlation Analysis (Data Cleaning):**
   - Read the CSV dataset.
   - Compute the Pearson correlation coefficient ($r$) between every pair of features (excluding `id`).
   - Find any pair of features where the absolute correlation is greater than 0.95 ($|r| > 0.95$).
   - For any such highly correlated pair, "drop" the feature that appears later in the column order of the CSV. (e.g., if `density` and `flexibility` are highly correlated, drop `flexibility`).
3. **Similarity Search (Recommendation):**
   - Using only the *remaining* feature columns, apply Min-Max normalization to each feature column (scale each column to $[0, 1]$ based on its minimum and maximum values).
   - Compute the Euclidean distance between the material with `id = 1` and all other materials based on these normalized features.
   - Identify the top 3 most similar materials (the 3 items with the lowest Euclidean distance to `id = 1`, excluding `id = 1` itself). Break any distance ties by preferring the lower `id`.
4. **Output:**
   - Your Rust program must output a JSON file at `/home/user/output.json` containing the dropped features and the top 3 similar item IDs in order of most similar to least similar.
   - The JSON must exactly match this structure:
     ```json
     {
       "dropped_features": ["feature_name_here"],
       "similar_to_1": [10, 42, 5]
     }
     ```

Run your Rust program so that the `/home/user/output.json` file is successfully created.