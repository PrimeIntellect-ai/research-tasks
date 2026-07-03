You are an AI assistant helping a mathematical researcher organize and analyze a dataset of derived formula features.

The researcher has a dataset located at `/home/user/raw_data.csv` and a pre-trained feature encoder model weights at `/home/user/encoder.pth`. You need to clean the data, enforce a schema, run inference using the reconstructed model, and perform a similarity search.

Follow these steps exactly:

1. **Data Schema Enforcement**:
   - Read `/home/user/raw_data.csv`.
   - Drop any rows where the `id` column cannot be parsed as a valid integer, and ensure the `id` column is cast to an integer type.
   - Keep only the rows where the `category` column is exactly `'A'`, `'B'`, or `'C'`. Drop all other rows.

2. **Missing Value Handling**:
   - The features are in columns `f1` through `f10`.
   - For each of these feature columns, impute any missing values (NaN) with the median of that specific column (computed over the dataset after step 1).

3. **Outlier Handling**:
   - For each feature column `f1` through `f10`, calculate the mean and standard deviation (use sample standard deviation, ddof=1).
   - Clip (limit) the values in each feature column to be within the range `[mean - 3*std, mean + 3*std]`.

4. **Model Architecture Reconstruction & Inference**:
   - Use PyTorch to define the encoder model. The architecture is:
     - A Linear (fully connected) layer taking 10 input features and outputting 8 features.
     - A ReLU activation function.
     - A Linear layer taking 8 input features and outputting 3 features.
   - Load the pre-trained weights from `/home/user/encoder.pth` into your model.
   - Convert the cleaned `f1` to `f10` features for all rows into a `torch.FloatTensor` and pass them through the model (in evaluation mode) to obtain a 3-dimensional embedding for each row.

5. **Similarity Search and Recommendation**:
   - Find the 3D embedding for the row where `id == 42`.
   - Compute the Cosine Similarity between the embedding of `id = 42` and the embeddings of all rows in your cleaned dataset.
   - Identify the top 5 `id`s that are most similar to `id = 42` (excluding `id = 42` itself).
   - Write these 5 `id`s to `/home/user/recommendations.txt` in descending order of similarity, one integer `id` per line.

Ensure you install any necessary Python libraries (like `pandas`, `torch`, `scikit-learn` etc.) if they are not already present.