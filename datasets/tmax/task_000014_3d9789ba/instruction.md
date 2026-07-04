You are an AI assistant helping a climate researcher organize a messy, deeply nested dataset of sensor readings. 

The raw data is located in `/home/user/raw_datasets/`. Over time, the data has been dumped into various archive formats (`.tar.gz`, `.tar`, `.zip`) scattered across multiple subdirectories. Inside these archives are various files, including sensor data (`.csv` and `.json`) and noise files (like `.txt`, `.jpg`, or `.tmp`).

The researcher needs you to extract, organize, and re-archive the valid data while creating a convenient symlink view for their analysis tools.

Your task is to write and execute a script (or a series of commands) to do the following:

1. **Find and Extract**: Recursively find all archives (`.tar.gz`, `.tar`, `.zip`) in `/home/user/raw_datasets/` and extract **only** the `.csv` and `.json` files from them. 
2. **Organize by Date**: All target files follow the naming convention `YYYY-MM-DD_sensor<ID>.<ext>` (e.g., `2023-01-15_sensorA.csv`). Move these extracted files into a new clean directory structure at `/home/user/clean_datasets/<YYYY>/<MM>/`.
3. **Create Path Views (Symlinks)**: The researcher's tools require data to be grouped by sensor. Create a directory `/home/user/sensor_views/`. For every file moved to `clean_datasets`, create a symbolic link in `/home/user/sensor_views/sensor<ID>/` pointing to the absolute path of the file in `clean_datasets`.
4. **Final Archive**: Create a final compressed tarball of the cleaned dataset at `/home/user/final_dataset.tar.gz` (this archive should contain the `clean_datasets` folder at its root, maintaining the `<YYYY>/<MM>/` structure).
5. **Logging**: Create a log file at `/home/user/summary.log` with the exact number of valid data files (`.csv` and `.json`) successfully processed and organized, written as a single integer.

**Requirements:**
- Do not extract or keep any files other than `.csv` and `.json`.
- The symlinks in `sensor_views` must use absolute paths.
- Ensure all created directories have the standard user read/write/execute permissions.