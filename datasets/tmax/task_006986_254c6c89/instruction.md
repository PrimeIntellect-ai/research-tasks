You are an ML engineer preparing training data for a new model. The data preparation pipeline is currently incomplete and failing. 

Your task is to fix and run the pipeline:

1. **Install Dependencies**: You may need to install required Python packages (`pandas`, `matplotlib`).
2. **Handle Missing Values and Outliers**: Edit the starter script at `/home/user/prep_data.py`. Read the dataset `/home/user/raw_data.csv`. 
   - Impute all missing values (NaNs) in the column `feature_A` with the median of `feature_A`.
   - Handle outliers in `feature_B` by capping them at the 95th percentile (any value strictly greater than the 95th percentile should be replaced with the exact 95th percentile value).
   - Save the processed DataFrame to `/home/user/cleaned_data.csv` (keeping the original columns, without the index).
3. **Experiment Tracking**: At the end of `/home/user/prep_data.py`, create a JSON file at `/home/user/experiment_log.json`. It must contain a dictionary with two keys:
   - `"imputed_count_A"`: (integer) The exact number of missing values that were imputed in `feature_A`.
   - `"cap_value_B"`: (float) The calculated 95th percentile value for `feature_B` used for capping, rounded to 2 decimal places.
4. **Fix the Visualization Script**: The script `/home/user/visualize.py` attempts to plot the cleaned data but fails in headless environments because it tries to open a GUI window using `plt.show()`. 
   - Modify `/home/user/visualize.py` to use the non-interactive `Agg` backend.
   - Save the plot to `/home/user/plot.png` instead of calling `plt.show()`.
5. **Run the Pipeline**: Execute both `/home/user/prep_data.py` and `/home/user/visualize.py` so that the final artifacts (`cleaned_data.csv`, `experiment_log.json`, and `plot.png`) are generated.