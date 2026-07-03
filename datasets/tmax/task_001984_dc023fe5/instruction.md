You are an AI assistant helping a materials researcher organize a messy dataset from a recent set of CNC milling experiments. 

The raw dataset is located in `/home/user/dataset/`. For each experiment run, there are three associated files sharing a common prefix (e.g., `001`):
1. `meta_<id>.json`: Contains metadata about the run (e.g., `{"exp_id": "EXP-A1", "operator": "Alice"}`).
2. `run_<id>.gcode`: The GCode file used to control the CNC mill.
3. `data_<id>.csv`: The raw sensor data collected during the run.

The researcher has noted several issues with the data:
- Due to a data logging error, the `meta_<id>.json` files were saved in various character encodings (some are UTF-8, some are UTF-16LE, and some are ISO-8859-1).
- The researcher needs to know the maximum Z-axis height reached during each run. This information is only available inside the `run_<id>.gcode` files. You will need to parse the GCode, extract all `Z` values from lines containing movement commands (e.g., `G0` or `G1` commands that include a `Z` parameter like `Z15.5` or `Z-2.0`), and find the maximum numeric value.

Your task is to process this dataset and output a clean version in `/home/user/dataset_clean/` by following these steps:

1. Create the directory `/home/user/dataset_clean/`.
2. Convert the contents of all `meta_<id>.json` files to UTF-8 and parse them to extract the `exp_id` and `operator`.
3. Parse each `run_<id>.gcode` file to find the maximum Z-height (`max_z` as a float).
4. Bulk rename and copy the `data_<id>.csv` files into `/home/user/dataset_clean/`. The new filename must be formatted as `<exp_id>_<operator>.csv` (e.g., `EXP-A1_Alice.csv`).
5. Generate a unified catalog file at `/home/user/dataset_clean/catalog.json`. This file must be a single JSON object where the keys are the `exp_id`s, and the values are objects containing `operator`, `max_z`, and `original_prefix`. To prevent partial writes in the event of a crash, ensure you write this JSON file atomically (e.g., write to a temporary file first, then use a filesystem move operation to overwrite/create the final `catalog.json`).

The structure of `/home/user/dataset_clean/catalog.json` MUST look exactly like this:
```json
{
  "EXP-A1": {
    "operator": "Alice",
    "max_z": 15.5,
    "original_prefix": "001"
  },
  "EXP-B2": {
    "operator": "Bob",
    "max_z": 10.0,
    "original_prefix": "002"
  }
}
```

Write whatever scripts you need to accomplish this. You can use any programming language available on the system.