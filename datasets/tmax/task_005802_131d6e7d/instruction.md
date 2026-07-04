You are an ML engineer preparing training data to build a meta-model that predicts inference latency based on model architecture. 

I have created a Python script at `/home/user/prepare_data.py` that is supposed to:
1. Load model metadata from `/home/user/metadata.csv`.
2. Load inference benchmark data from `/home/user/benchmarks.csv`.
3. Join the two datasets on the model ID.
4. Aggregate the data to find the mean `inference_ms` per `architecture`.
5. Save the aggregated tabular data to `/home/user/summary.csv`.
6. Generate a bar chart of these averages and save it to `/home/user/benchmark_plot.png`.

However, the script is currently producing an empty `summary.csv` and a completely blank plot. Furthermore, it occasionally throws display/backend warnings.

Your task is to debug and fix `/home/user/prepare_data.py` so that it successfully performs the operations above. 

Requirements for the output:
- `/home/user/summary.csv` must contain exactly two columns: `architecture` and `inference_ms` (in that order), containing the grouped average inference times. It must include a header row.
- `/home/user/benchmark_plot.png` must be a valid, non-empty PNG image file containing the plot. Ensure the script can run in our headless environment without crashing or requiring an X server.

Do not modify the input CSV files. Only modify `/home/user/prepare_data.py`. Run the script to generate the final outputs.