You are an AI assistant acting as a Machine Learning Engineer. You need to prepare some training data benchmarks, reconstruct a model for inference, and fix a plotting script that is failing to output correctly.

All your work should be done in `/home/user/workspace/`.

1. **Model Reconstruction & Inference**: 
   You have been provided with a PyTorch state dictionary saved at `/home/user/workspace/model.pth`. 
   The original model code was lost, but we know it is a simple Multi-Layer Perceptron (MLP) containing exactly two Linear layers with a ReLU activation in between.
   Inspect the keys and shapes in `model.pth` to reconstruct the exact `torch.nn.Module` or `torch.nn.Sequential` architecture.
   
2. **Inference Benchmarking**:
   You have a dataset at `/home/user/workspace/data.csv` consisting of 1000 rows of numerical features (no header).
   Write a Python script to load the data, load the reconstructed model weights, and run forward passes (inference) for the entire dataset without computing gradients (`torch.no_grad()`).
   Benchmark the total time it takes to process the entire dataset for three different batch sizes: `1`, `32`, and `128`.
   Save these results to `/home/user/workspace/benchmark.csv` with exactly two columns: `batch_size` and `time_seconds`. Ensure the rows correspond to the batch sizes in ascending order.

3. **Fix the Plotting Script**:
   There is a script at `/home/user/workspace/plot.py` designed to visualize these benchmarks. However, it currently tries to render an interactive window (which fails in a headless server environment) and does not save the plot.
   Modify `plot.py` so that it runs successfully in a headless environment and saves the plot to `/home/user/workspace/benchmark.png`. Do not alter the core logic of what is being plotted.

4. **Experiment Tracking**:
   Finally, save your benchmark results into a JSON file at `/home/user/workspace/experiment_log.json`. The JSON file should contain a single dictionary mapping the batch sizes (as strings: `"1"`, `"32"`, `"128"`) to their corresponding total inference time in seconds (as floats).

Please implement the missing pieces, run the benchmarks, fix the plot script, and generate the required outputs.