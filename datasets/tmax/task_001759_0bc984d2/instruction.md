You are an integration developer responsible for testing a new Python API client that handles data synchronization. 

Your workspace is located at `/home/user/workspace`. Inside, you will find a Python project directory called `api-client` and two raw data files: `data1.txt` and `data2.txt`.

Currently, the project is broken. Your tasks are:

1. **Fix Dependencies:** The `pyproject.toml` in `/home/user/workspace/api-client` has a broken configuration that prevents installation and testing. Fix the file so it correctly installs the package and its test dependencies (`pytest` and `hypothesis`).
2. **Run Property Tests:** Once fixed, install the package locally and run `pytest /home/user/workspace/api-client/test_client.py`. Ensure the property-based tests pass. Output the test result log to `/home/user/workspace/test_results.log`.
3. **Data Processing:** Using standard Linux command-line tools (bash built-ins, coreutils):
   - Sort both `/home/user/workspace/data1.txt` and `/home/user/workspace/data2.txt` alphabetically.
   - Find the lines that are strictly unique to `data2.txt` (lines that appear in `data2.txt` but NOT in `data1.txt`). Save these lines to `/home/user/workspace/unique_data.txt`.
4. **Checksum:** Calculate the SHA256 checksum of `/home/user/workspace/unique_data.txt` and save ONLY the checksum hash (no filenames or extra whitespace) to `/home/user/workspace/checksum.txt`.

Ensure all requested output files (`test_results.log`, `unique_data.txt`, `checksum.txt`) are located exactly where specified.