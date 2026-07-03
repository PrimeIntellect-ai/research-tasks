I am a researcher organizing a dataset of mathematical vectors, and I need your help filtering them based on a pre-trained neural network.

I have a set of 50 `.npy` files in the directory `/home/user/dataset/`. Each file contains a 1D NumPy array of length 10.
I also have a file containing the weights of a trained Multilayer Perceptron (MLP) at `/home/user/model_weights.npz`. 

The MLP has the following architecture:
1. An input layer of size 10.
2. A hidden layer of size 5 with a ReLU activation function.
3. An output layer of size 1 with no activation function (raw logit).

The weights file contains the following keys for the NumPy arrays:
- `W1` (shape: 10, 5) and `b1` (shape: 5) for the first layer (computed as `x @ W1 + b1`).
- `W2` (shape: 5, 1) and `b2` (shape: 1) for the second layer.

Your task is to:
1. Install any necessary dependencies (e.g., PyTorch, NumPy) in my environment.
2. Reconstruct the model architecture using PyTorch and load the weights from `/home/user/model_weights.npz`.
3. Run inference on all 50 samples in `/home/user/dataset/`.
4. Based on the model's output:
   - If the output value is strictly greater than 0, move the `.npy` file to `/home/user/positive_cases/`.
   - If the output value is less than or equal to 0, move the `.npy` file to `/home/user/negative_cases/`.
5. Create a summary file at `/home/user/summary.txt` with exactly the following format:
```
Positive: [Count of positive cases]
Negative: [Count of negative cases]
```

Make sure the directories `/home/user/positive_cases/` and `/home/user/negative_cases/` exist before moving the files.