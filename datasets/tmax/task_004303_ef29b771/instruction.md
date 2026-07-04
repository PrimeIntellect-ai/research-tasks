I need you to help me organize a messy directory of legacy project assets. I have an archive located at `/home/user/legacy_assets.tar.gz` containing several JSON configuration files scattered across different subdirectories.

Please perform the following steps:
1. Extract the contents of `/home/user/legacy_assets.tar.gz` into a new directory called `/home/user/processing`.
2. Write a Python script at `/home/user/organize.py` that processes these files. The script must:
   - Find all `.json` files within `/home/user/processing` (and its subdirectories).
   - For each file, acquire an exclusive system-level file lock using `fcntl.flock(file_descriptor, fcntl.LOCK_EX)` before reading/writing, to simulate safe concurrent access. 
   - Parse the JSON data, inject a new key `"processed"` with the boolean value `true`.
   - Convert the data to YAML format.
   - Save the new YAML file in the same directory as the original, but bulk-rename it by prepending `asset_` to the original filename and changing the extension to `.yaml` (e.g., `config.json` becomes `asset_config.yaml`).
   - Release the lock and delete the original `.json` file.
3. Run the script. (You may need to install the `pyyaml` package).
4. Create a new ZIP archive at `/home/user/clean_assets.zip` that contains ONLY the newly created `.yaml` files. The zip file should not contain the directory structure, just the flat `.yaml` files at its root.

Let me know when you have created `/home/user/clean_assets.zip` and `/home/user/organize.py`.