You are a data analyst tasked with processing sensor data using a pre-trained custom machine learning model. The original model was created in a proprietary system, but its architecture and weights have been exported to a JSON file.

Your objective is to build a reproducible Python pipeline that sets up the analysis environment, reconstructs the model architecture, and runs inference on a provided CSV dataset. 

Here are the details:
1. **Input Data**: Located at `/home/user/data/input.csv`. It contains 4 columns: `id`, `sensor_A`, `sensor_B`, and `sensor_C`.
2. **Model Definition**: Located at `/home/user/model/network.json`. It describes a simple Multilayer Perceptron (MLP) with Dense layers. 
    - The `weights` matrices are provided in a shape where you multiply the input matrix by the weights (i.e., `Input @ Weights + Biases`).
    - The network uses standard activations: `relu` ( $f(x) = \max(0, x)$ ) and `sigmoid` ( $f(x) = \frac{1}{1 + e^{-x}}$ ).
3. **Your Task**:
    - Write a Python script at `/home/user/scripts/infer.py` that reads the input data and the model definition.
    - Implement a forward pass of this neural network from scratch (you may use NumPy, but no high-level ML libraries like PyTorch, TensorFlow, or scikit-learn).
    - For each row, calculate the final probability. If the probability is $\ge 0.5$, the prediction is `1`, otherwise `0`.
    - Save the results to `/home/user/output/predictions.csv`. Ensure the output directory exists before writing.
    - The output CSV must have exactly two columns: `id` and `prediction`.

Please execute your script and ensure the output file is generated correctly.