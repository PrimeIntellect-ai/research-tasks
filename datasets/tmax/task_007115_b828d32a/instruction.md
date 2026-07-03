I am a researcher organizing a messy dataset of sensor readings, and I need your help filtering and archiving the useful data.

I have an archive located at `/home/user/datasets/experiments.tar.gz`. Inside this archive, there are several directories named `exp_001`, `exp_002`, etc. 
Each directory corresponds to a single experiment and contains two files:
1. `meta.json`: A JSON file containing metadata about the experiment.
2. `readings.csv`: A CSV file containing the actual sensor data, with the header `id,timestamp,intensity,wavelength`.

I need you to do the following:
1. Extract the dataset.
2. Identify all experiments where the `meta.json` file has exactly `"status": "success"` AND `"experiment_type": "spectroscopy"`. Ignore any experiments that failed or are of a different type.
3. For these matching experiments, parse their `readings.csv` files and filter for rows where the `intensity` value (the 3rd column) is strictly greater than `100`.
4. Combine all the filtered rows from the matching experiments into a single CSV file located at `/home/user/high_intensity.csv`. This new file must contain the header `id,timestamp,intensity,wavelength` exactly once at the top. The data rows can be in any order.
5. Finally, create a new compressed archive (gzip compressed tarball) at `/home/user/processed_spectroscopy.tar.gz`. This archive must contain:
   - The combined `high_intensity.csv` file (at the root of the archive).
   - Only the `meta.json` files of the matching (successful spectroscopy) experiments, maintaining their original folder structure (e.g., `exp_001/meta.json`). Do not include the original CSVs or any files from non-matching experiments in this new archive.

Please perform these operations. The success of the task will be verified by inspecting `/home/user/high_intensity.csv` and the contents of `/home/user/processed_spectroscopy.tar.gz`.