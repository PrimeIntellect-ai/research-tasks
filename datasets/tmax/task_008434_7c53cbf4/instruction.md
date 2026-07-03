You are a data scientist tasked with cleaning a corrupted dataset, extracting features using linear algebra, and running inference through a manually reconstructed neural network. 

Your tasks are:

1. **Environment Setup:** 
   Install necessary packages for numerical operations and data handling in Python (e.g., `numpy`). 

2. **Data Cleaning:**
   You have a raw dataset at `/home/user/data/raw_features.csv`. Due to storage errors, some lines are corrupted. 
   Filter the dataset to remove:
   - Any line containing the string `CORRUPT`.
   - Any line that does not have exactly 10 comma-separated numeric values.
   Preserve the original relative order of the valid rows.

3. **Feature Engineering:**
   Load the cleaned 10-dimensional feature matrix $X$.
   - Multiply $X$ by the projection matrix $P$ located at `/home/user/data/projection.csv`. (Compute $X_{proj} = X \times P$). The projection matrix is 10x5.
   - Apply row-wise L2 normalization to $X_{proj}$ so that the Euclidean norm of each row becomes exactly 1. Let this normalized matrix be $X_{norm}$.

4. **Model Architecture Reconstruction and Inference:**
   You are provided with a pre-trained simple Multi-Layer Perceptron (MLP) weights file at `/home/user/data/weights.json`. The JSON contains `W1`, `b1`, `W2`, and `b2`.
   - Perform a forward pass using the equations:
     - Hidden Layer: $H = \text{ReLU}(X_{norm} \times W1 + b1)$
     - Output Layer: $Y = H \times W2 + b2$
   - Note: $\text{ReLU}(x) = \max(0, x)$.

5. **Reporting:**
   For each row in $Y$, compute the predicted class index using the argmax function (0-indexed).
   Save the final predicted class indices as a single column of integers to `/home/user/predictions.txt`, one per line, maintaining the sequence of the cleaned rows.

Your final output must be precisely located at `/home/user/predictions.txt`. Do not include any headers or indices in the output file, just the predicted integer classes.