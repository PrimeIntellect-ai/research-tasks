You are an AI assistant helping a machine learning engineer prepare training data. 

I have an ETL pipeline script written in Python (`/home/user/scripts/extract.py`), but it's currently producing empty output files, similar to a misconfigured plotting library yielding blank images. The script reads raw CSV files and performs initial transformations.

I need you to create a complete Bash orchestration script at `/home/user/pipeline.sh` that fixes this issue, runs the pipeline, and performs feature extraction. 

Your Bash script (`/home/user/pipeline.sh`) must perform the following exactly:
1. **Dependency Installation**: Create a Python virtual environment at `/home/user/venv` and install `pandas`.
2. **ETL Execution**: 
   - Inspect `/home/user/scripts/extract.py` to understand why it's outputting empty files and configure the environment inside your Bash script to fix this.
   - Create a directory `/home/user/processed/`.
   - Run the fixed `extract.py` on both `/home/user/raw_data/dataset1.csv` and `/home/user/raw_data/dataset2.csv`, saving the outputs to `/home/user/processed/dataset1_proc.csv` and `/home/user/processed/dataset2_proc.csv`.
3. **Feature Selection & Merging**:
   - Merge the two processed CSV files.
   - Perform feature selection to keep ONLY the following columns: `id`, `feature_alpha`, `feature_beta`, and `target`.
   - Ensure there is only exactly one header row in the final merged output.
   - Save the final dataset to `/home/user/final_features.csv`.
4. **Validation**: 
   - Count the total number of data rows in `/home/user/final_features.csv` (excluding the header).
   - Save this integer to `/home/user/row_count.txt`.

Once you have written `/home/user/pipeline.sh`, make sure it is executable and run it so the final outputs are generated.