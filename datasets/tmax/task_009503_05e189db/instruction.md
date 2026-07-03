You are an MLOps engineer tasked with tracking down an anomaly in a recent batch of experiment artifacts. 

You have been provided with an artifact log at `/home/user/experiments.csv`. This file contains the serialized inputs and weights of a simple single-layer neural network used to generate embeddings during the experiments.

Your task is to write a Rust program that reads this file, reconstructs the embeddings, aggregates them, and performs a similarity search to find the experiment group that best matches a target vector.

Here are the specific requirements:

1. **Input Data**: 
   The CSV at `/home/user/experiments.csv` has three columns: `exp_group` (string), `input_vector` (JSON string of a 3-element float array), and `weight_matrix` (JSON string of a 3x3 float array, representing a list of 3 rows).

2. **Embedding Computation**:
   For each row in the CSV, compute the output embedding. The model architecture is a single linear projection followed by a ReLU activation.
   - Let `x` be the `input_vector` (1x3).
   - Let `W` be the `weight_matrix` (3x3).
   - Compute `y = x * W` (standard vector-matrix multiplication, where `y_j = sum_i (x_i * W_ij)`).
   - Apply ReLU: `embedding_j = max(0.0, y_j)`.

3. **Tabular Aggregation**:
   Group the computed embeddings by `exp_group`. For each group, calculate the mean embedding (average each of the 3 dimensions across all embeddings in that group).

4. **Similarity Search**:
   You have a target anomaly vector: `[1.0, 0.5, 0.2]`.
   Calculate the Cosine Similarity between the target vector and the mean embedding of each `exp_group`.

5. **Output**:
   Identify the `exp_group` with the highest cosine similarity to the target vector.
   Write ONLY the name of this `exp_group` (as plain text, no quotes or extra formatting) to a file named `/home/user/closest_experiment.txt`.

You may create a standard Cargo project in `/home/user/mlops_tool` to write your Rust code. You can use standard crates like `serde`, `serde_json`, and `csv`.