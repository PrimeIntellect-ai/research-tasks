I am a researcher organizing a messy dataset from a recent large-scale physics simulation, and I need your help to consolidate the data, reconstruct a missing predictive model, run inference, and analyze the feature correlations. I also need to ensure the pipeline is reproducible.

Here is the situation:
In `/home/user/experiment_data/raw/`, there are 50 CSV files (`sim_0.csv` to `sim_49.csv`). Each contains 10,000 rows of un-headered data with 20 continuous numerical features.
In `/home/user/experiment_data/model/`, there is a JSON file `architecture_and_weights.json` containing the weights and biases for a simple multi-layer perceptron (MLP). The researcher who trained it didn't save the PyTorch model object, only the raw numpy arrays as lists in the JSON. 

Your tasks are to:
1. **Large-scale Storage Management**: Read all 50 CSV files, concatenate them in order (from `sim_0.csv` to `sim_49.csv`), assign column names `feature_0` through `feature_19`, and save the resulting dataset as a single Parquet file at `/home/user/experiment_data/processed/consolidated.parquet`. Use PyArrow or Pandas.
2. **Model Reconstruction**: The model was a PyTorch neural network with the following architecture:
   - Input layer (20 features)
   - Fully connected hidden layer (32 units) with a ReLU activation
   - Fully connected output layer (1 unit) with no activation
   The `architecture_and_weights.json` contains keys: `hidden.weight`, `hidden.bias`, `output.weight`, `output.bias`. 
   Write a Python script to reconstruct this PyTorch model and load these exact weights.
3. **Inference & Correlation Analysis**: Pass the entire consolidated dataset (all 500,000 rows) through the reconstructed model to get a single prediction value for each row. Then, compute the Pearson correlation coefficient between each of the 20 input features and the predicted output.
4. **Reporting**: Save the correlation results to `/home/user/experiment_data/results/correlations.json`. The file should be a valid JSON dictionary mapping the feature name to its Pearson correlation coefficient with the prediction, rounded to 4 decimal places. For example: `{"feature_0": 0.1234, "feature_1": -0.5678, ...}`.
5. **Pipeline Reproducibility**: Create a script `/home/user/experiment_data/verify_pipeline.py` that, when run without arguments, performs the inference and correlation calculation on the parquet file and exits with code 0 if successful.

Please create all necessary directories if they do not exist (`processed` and `results`). You may write intermediate Python scripts to perform these actions. Ensure your final `correlations.json` exactly matches the required structure.