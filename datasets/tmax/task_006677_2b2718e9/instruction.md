You are a data analyst responsible for evaluating a mathematical model on several CSV datasets. A previous team member left a Python script `/home/user/workspace/model_eval.py` that is supposed to train a simple linear model, benchmark its inference performance, validate the output by calculating the Mean Squared Error (MSE), track the results in a JSON file, and generate a plot.

However, the script has several issues:
1. **Dependency & Environment:** You need to install the required packages. A `requirements.txt` is provided. Create and use a virtual environment at `/home/user/workspace/venv`.
2. **Plotting Configuration:** The script produces an error or hangs when plotting because it is running on a headless server. You must configure `matplotlib` to use the `Agg` backend *before* importing `pyplot` so that it successfully saves the plots as PNG files.
3. **Inference Benchmarking:** The current benchmarking measures the entire execution time (including data loading and model training). You must modify the script so that `inference_time_sec` measures *only* the execution time of the `predict(coeffs, x)` function call.
4. **Model Output Validation:** The MSE calculation in the script is mathematically incorrect. Fix it to calculate the true Mean Squared Error.
5. **Experiment Tracking:** The script currently overwrites `/home/user/workspace/results.json` on each run. You must fix it so that it reads the existing JSON array (if the file exists), appends the new result object, and writes the array back. If the file doesn't exist, it should create a new list.

**Your Goal:**
1. Fix all the bugs in `/home/user/workspace/model_eval.py`.
2. Run the script on all three provided datasets (`data1.csv`, `data2.csv`, `data3.csv`) located in `/home/user/workspace/`.

**Verification:**
An automated test will check:
- The existence of `/home/user/workspace/results.json` containing a valid JSON array of exactly 3 objects.
- Each object must have `"dataset"` (e.g., "data1.csv"), `"mse"` (correctly computed), and `"inference_time_sec"` (which should be very small, reflecting only the inference step).
- The generated plots (`plot_data1.png`, `plot_data2.png`, `plot_data3.png`) must exist and not be empty.