You are a data scientist working on an edge-computing pipeline written in C. We have a pipeline that extracts features from two different sensors, performs dimensionality reduction (PCA), and runs inference using a simple pre-trained linear model.

Recently, our team tried to port the data joining and inference logic into C to run on a restricted edge device. Unfortunately, the developer left the project incomplete. 

Your task is to write a C program from scratch at `/home/user/pipeline.c` that performs the following steps:

1. **Multi-source Data Joining**: 
   Read `/home/user/sensor1.csv` (Columns: `id,f1,f2`) and `/home/user/sensor2.csv` (Columns: `id,f3,f4`). 
   Join the records on the `id` column. Note that the rows might not be in the same order in both files! You must correctly match them. The combined feature vector should be `[f1, f2, f3, f4]`.

2. **Dimensionality Reduction**:
   Read the projection matrix from `/home/user/pca_weights.txt`. It contains 4 rows and 2 columns of floats. Multiply your 1x4 feature vector by this 4x2 matrix to get a 1x2 reduced feature vector.

3. **Model Inference**:
   Read the model weights from `/home/user/model_weights.txt`. It contains 2 rows and 1 column. Multiply your 1x2 reduced vector by this 2x1 weight matrix to get a single scalar `score`.

4. **Output**:
   Write the final scores to `/home/user/predictions.csv` with the format:
   ```
   id,score
   ```
   Print the output sorted by `id` in ascending order. Format the score to exactly one decimal place (e.g., `12.5`).

You must write the code in C, compile it (e.g., `gcc -o pipeline pipeline.c`), and run it to produce the final `predictions.csv` file. Do not use Python or other languages for the final data processing, though you may use them to inspect the data.