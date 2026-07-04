You are a data analyst who needs to process a large CSV dataset using a lightweight machine learning model. You have been given the model's architecture and weights, but no inference code. 

Your task is to write the inference code, benchmark its performance, and orchestrate the process using Bash.

Here is the setup:
1. There is a dataset located at `/home/user/dataset.csv`. It contains 10,000 rows with a header row `id,f1,f2,f3,f4`. All features (`f1` to `f4`) are numerical.
2. The model weights are provided in a JSON file at `/home/user/weights.json` with the following structure:
   ```json
   {
     "weights": [0.5, -1.2, 3.4, 0.8],
     "bias": -0.5
   }
   ```
3. The model architecture is a simple linear classifier. The raw score is calculated as the dot product of the feature vector and the weights, plus the bias. If the raw score is strictly greater than 0, the prediction is `1`, otherwise `0`.

You need to create a Bash script at `/home/user/run_pipeline.sh` that performs the following steps when executed:
1. Creates a Python virtual environment in `/home/user/venv`.
2. Activates the virtual environment and installs the `numpy` and `pandas` packages.
3. Calls a Python script `/home/user/predict.py` (which you must also create).

The Python script `/home/user/predict.py` must:
1. Load the dataset and the weights.
2. Reconstruct the model and run inference on the entire dataset to generate predictions.
3. Precisely measure the time taken to perform *only* the inference step (i.e., the mathematical calculation of predictions, excluding data loading and file I/O).
4. Save the predictions to `/home/user/predictions.csv`. The file should have a header `id,prediction` and contain the respective integer IDs and the integer predictions (0 or 1).
5. Append the measured inference time to a log file at `/home/user/metrics.txt` in the exact format: `inference_time_ms:<time_in_milliseconds>` (e.g., `inference_time_ms:14.25`).

Ensure that your Bash script is executable (`chmod +x /home/user/run_pipeline.sh`) and runs the entire pipeline end-to-end without any user interaction. Run your script to generate the final outputs.