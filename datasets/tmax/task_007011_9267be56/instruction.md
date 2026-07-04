You have been given a small data project in `/home/user/data_project`. It contains a raw dataset `raw_data.csv` and a Python script `train_model.py`. 

Your goal is to build a simple ETL pipeline and fix a broken analysis script. 

Specifically, you need to:
1. Create a Bash script named `/home/user/data_project/prepare_data.sh` that processes `raw_data.csv` and outputs `processed_data.csv` in the same directory. The raw dataset has five columns: `id,feature1,feature2,feature3,target`. Your bash script must:
   - Keep only the columns `id`, `feature1`, `feature2`, and `target` (in that order).
   - Remove any rows (except the header) where the `target` value is missing (empty string).
   - Write the filtered data to `processed_data.csv`.
2. The provided `train_model.py` script is supposed to train a Logistic Regression model on `processed_data.csv`, calculate the AUC score, and generate an ROC curve plot (`roc_curve.png`). However, it currently crashes in a headless terminal environment because it is configured to use an interactive matplotlib backend (`TkAgg`). Modify `train_model.py` to use a non-interactive backend so that it successfully saves the plot.
3. Run your bash script and then run the python script.

When you are done, the directory `/home/user/data_project` should contain:
- `prepare_data.sh`
- `processed_data.csv`
- `train_model.py` (fixed)
- `roc_curve.png`
- `metrics.txt`