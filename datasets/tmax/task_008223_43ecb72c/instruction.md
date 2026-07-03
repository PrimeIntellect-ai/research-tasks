You are a data analyst tasked with processing a batch of sensor data using a pre-trained neural network. 

In `/home/user/data`, there are several CSV files containing sensor readings. Each CSV has three columns: `feature1`, `feature2`, and `feature3`.
In `/home/user/model/weights.json`, there are the extracted weights and biases of a simple Multi-Layer Perceptron (MLP) binary classifier. 

The network architecture is as follows:
- Input layer: 3 features (in the order of feature1, feature2, feature3).
- Hidden layer: 4 neurons, with a ReLU activation function.
- Output layer: 1 neuron, with a Sigmoid activation function.

Your task is to:
1. Set up your Python environment by installing any necessary standard data science libraries (e.g., `numpy`, `pandas`) using pip.
2. Write a Python script at `/home/user/run_inference.py` that reconstructs this network architecture from `weights.json`. The JSON contains keys `W1`, `b1`, `W2`, `b2` corresponding to the weights and biases of the hidden and output layers respectively.
3. Process every CSV file in `/home/user/data/` through this model.
4. For each row in a CSV, calculate the output probability. If the probability is >= 0.5, the prediction is 1 (positive); otherwise, it is 0 (negative).
5. Calculate the positive prediction rate (number of positive predictions / total rows) for each file.
6. Output the results to `/home/user/results.csv`. The output CSV must have exactly two columns: `filename` (just the base name of the file, e.g., `sensor_A.csv`) and `positive_rate` (rounded to 4 decimal places). The rows must be sorted alphabetically by `filename`.

Ensure your script is fully self-contained and runs without errors. After writing it, execute it so that `/home/user/results.csv` is generated.