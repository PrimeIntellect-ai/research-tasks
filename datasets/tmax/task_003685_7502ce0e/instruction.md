You are an MLOps engineer tasked with analyzing experiment artifacts and reconstructing the best model architecture for testing. 

You have been provided with an experiment log file at `/home/user/experiments.csv`. This file contains the results of various model training runs.

Please perform the following steps:
1. **Analyze the Experiments**: Read `/home/user/experiments.csv`. Group the runs by `num_layers` and `hidden_size` to find the configuration with the highest mean `accuracy`.
2. **Hypothesis Testing**: Perform an independent two-sample t-test (Welch's t-test, assuming unequal variances) comparing the accuracies of all runs using the *best* configuration against the *baseline* configuration (defined as `num_layers=2` and `hidden_size=64`). Extract the p-value.
3. **Model Reconstruction**: Using PyTorch, reconstruct a Multi-Layer Perceptron (MLP) matching the *best* configuration. The model must adhere to these specifications:
    - Input dimension: 10
    - Total number of Linear layers: `num_layers` (from the best config)
    - The first `num_layers - 1` Linear layers should output a dimension of `hidden_size` and be immediately followed by a ReLU activation function.
    - The final Linear layer should output a dimension of 2 (no activation after it).
    - Crucial for verification: Initialize ALL weights in every Linear layer to exactly `0.01`, and ALL biases to `0.0`.
4. **Mock Inference**: Perform a forward pass through your reconstructed model using an input tensor of shape `(1, 10)` where all elements are `1.0`. Calculate the sum of the values in the output tensor.
5. **Experiment Tracking**: Save your findings to a JSON file at `/home/user/experiment_summary.json` with exactly the following keys and data types:
    - `"best_num_layers"`: integer
    - `"best_hidden_size"`: integer
    - `"p_value"`: float (rounded to 4 decimal places)
    - `"inference_sum"`: float (rounded to 4 decimal places)

Ensure the JSON file is correctly formatted and located exactly at `/home/user/experiment_summary.json`.