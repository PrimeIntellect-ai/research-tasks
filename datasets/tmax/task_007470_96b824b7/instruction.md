You are an ML engineer tasked with preparing a training data pipeline. We need to set up the numerical library environment properly, find the best feature based on correlation, and run a baseline inference script using that feature.

Your goal is to write a Bash script at `/home/user/run_pipeline.sh` that automates this process.

Here are the requirements for `/home/user/run_pipeline.sh`:
1. It must run with `bash` (include the appropriate shebang).
2. It must configure the numerical libraries by exporting the following environment variables:
   - `OPENBLAS_NUM_THREADS=2`
   - `OMP_NUM_THREADS=2`
3. It should execute the provided Python script `/home/user/scripts/get_correlations.py` passing `/home/user/data/dataset.csv` as the only argument. This Python script prints the correlation of each feature with the `target` column in the format `feature_name:correlation_value`.
4. Your Bash script must parse the output of `get_correlations.py` to identify the feature with the highest **absolute** correlation with the `target`.
5. Finally, your Bash script must execute the provided Python script `/home/user/scripts/run_inference.py`. This script expects two arguments: the path to the dataset (`/home/user/data/dataset.csv`) and the name of the most correlated feature you found in step 4.
6. Capture the standard output of `run_inference.py` and redirect it to `/home/user/predictions.txt`.

The scripts and data are already in the system, but you need to write the orchestrating bash script and ensure it generates the correct output. Do not modify the python scripts or dataset.

Run your script once it's created to generate `/home/user/predictions.txt`.