You are an MLOps engineer tasked with fixing an experiment tracking pipeline and finding the most relevant historical experiment for a new run. 

We use a script located at `/home/user/generate_vector.py` to generate an artifact embedding (a 5-dimensional numerical vector) for our current machine learning pipeline. However, the generation has been non-reproducible due to multi-threading variations in numerical libraries and unset random seeds.

Your task has three parts:

1. **Pipeline Reproducibility & Library Configuration**:
   Execute `/home/user/generate_vector.py` to generate the target vector. For the script to produce a reproducible and valid output, you must configure the environment to force single-threaded execution for OpenMP and OpenBLAS (set both `OMP_NUM_THREADS` and `OPENBLAS_NUM_THREADS` to `1`). Additionally, you must set the environment variable `NP_SEED` to `1337` before running the script. Save the standard output of this script (a comma-separated list of 5 floats) to `/home/user/target_vector.txt`.

2. **Similarity Search & Recommendation**:
   There is an experiment tracking database exported as a CSV file at `/home/user/past_experiments.csv`. The CSV has headers: `exp_id,v1,v2,v3,v4,v5`. 
   Write a Python script (e.g., `/home/user/search.py`) that reads the target vector from `/home/user/target_vector.txt` and the historical vectors from `/home/user/past_experiments.csv`. Calculate the **Cosine Similarity** between the target vector and every historical vector.

3. **Experiment Tracking Output**:
   Identify the `exp_id` of the historical experiment that is most similar (highest cosine similarity) to the target vector. Write *only* the string value of this `exp_id` to a file located at `/home/user/best_match.txt`. No newline character is necessary, but it is acceptable.

Ensure all file paths are exact and your Python script works entirely within standard libraries or widely used numerical libraries like `numpy` which is already installed.