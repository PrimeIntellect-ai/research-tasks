You are acting as a machine learning engineer preparing training data and reports. 

We have a dataset located at `/home/user/dataset.csv` with columns `id`, `category`, `f1`, and `f2`. 
We also have a saved PyTorch model state dict at `/home/user/model.pth`. The original code for the model was lost, but we know it's a simple Multi-Layer Perceptron (MLP) that takes `f1` and `f2` as inputs (size 2), has a single hidden layer of size 16 with a ReLU activation, and an output layer of size 1.

Your task is to write a Python script at `/home/user/process.py` that performs the following steps:
1. Load `/home/user/dataset.csv`.
2. Reconstruct the PyTorch model architecture and load the weights from `/home/user/model.pth`.
3. Run inference on the `f1` and `f2` features (as float32) for the entire dataset to generate predictions.
4. Add these predictions to the dataset as a new column named `pred`.
5. Group the data by `category` and calculate the mean of the `pred` column for each category.
6. Save this aggregated result to `/home/user/summary.csv`. The CSV should have exactly two columns: `category` and `mean_pred`.
7. Generate a bar chart of `mean_pred` across the different categories and save it to `/home/user/plot.png`. 

**Important:** We are running this on a headless Linux server without a display. Make sure your plotting code handles this properly so it doesn't crash or produce a blank plot (e.g., configure the matplotlib backend appropriately).