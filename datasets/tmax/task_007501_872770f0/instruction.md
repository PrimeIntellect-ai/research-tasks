You are a developer tasked with debugging a failing data processing pipeline.

The pipeline is located in `/home/user/data_pipeline`. It is designed to iterate over all JSON files in the `data/` directory, process them using `process.py`, and aggregate the results into `output/combined.json`. 

Currently, running the build script (`./build.sh`) fails due to several issues:
1. **Missing Configuration**: The `process.py` script relies on a `secret_key` in `config.json`. A previous developer accidentally removed this key and committed the change. You need to investigate the git history of the repository, find the original secret key, and restore it in `config.json`.
2. **Build Script Errors**: The shell script (`build.sh`) crashes when encountering certain filenames in the `data/` directory. You must fix the script so it handles all files correctly without renaming any files in the `data/` directory.
3. **Serialization/Encoding Issues**: One of the data files was saved with a different encoding, causing the Python script to fail when reading it. You need to modify `process.py` (or the file itself) to correctly read all the JSON data.

Your goal is to fix the pipeline so that running `./build.sh` completes without errors and correctly generates the `/home/user/data_pipeline/output/combined.json` file.

**Requirements**:
- Do not rename, delete, or move any files inside the `data/` directory.
- The `secret_key` in `config.json` must exactly match the value from the git history.
- After running `./build.sh`, `/home/user/data_pipeline/output/combined.json` must contain a JSON array with the data from all files in the `data/` directory, and each object must include the `auth` key with the recovered secret.