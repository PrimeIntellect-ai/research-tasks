You are a data scientist working on a novel project that relates molecular graph topologies to their simulated Raman spectroscopy signals. 

You have been provided with a dataset at `/home/user/dataset.npz`. This file contains three numpy arrays:
- `adj_matrices`: A 3D array of shape `(N, V, V)` containing the unweighted, undirected adjacency matrices of `N` molecular graphs.
- `signals`: A 2D array of shape `(N, 1000)` containing the simulated spectroscopy signal intensities.
- `frequencies`: A 1D array of shape `(1000,)` containing the frequency values corresponding to the bins in `signals`.

Your task is to write and execute a Python script `/home/user/analyze.py` that performs the following workflow:

1. **Graph Analysis:** For each of the `N` adjacency matrices, calculate the graph diameter (the longest shortest-path distance between any pair of nodes). You can assume all graphs are fully connected.
2. **Signal Processing:** The signals are noisy. Smooth each of the `N` signals using a simple moving average of window size 5. Specifically, the smoothed signal of length 996 should be computed such that the value at index `i` is the mean of the original signal values from index `i` to `i+4` (inclusive). 
3. **Peak Extraction:** For each smoothed signal, find the index of its maximum intensity. Determine the corresponding peak frequency. The frequency corresponding to the smoothed signal at index `i` is the original frequency at index `i+2`.
4. **Model Fitting:** Fit a simple linear regression model to predict the Peak Frequency ($y$) based on the Graph Diameter ($x$). Find the ordinary least squares `slope` and `intercept`.
5. **Validation:** Calculate the Mean Absolute Error (MAE) of your model's predictions on the same dataset.
6. **Output:** Save your final metrics to `/home/user/results.json` with the following structure, rounding all numerical values to 4 decimal places:
```json
{
  "slope": 12.3456,
  "intercept": 123.4567,
  "mae": 1.2345
}
```

Ensure your script handles everything end-to-end and creates the JSON file when run.