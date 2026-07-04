You are tasked with automating a step in a CI/CD pipeline to migrate a legacy data processing script from Python 2 to Python 3.

You have been given a workspace at `/home/user/migration`. Inside this directory, you will find:
1. `input.json`: A legacy dataset.
2. `migrate.py`: A Python 2 script that migrates the schema of `input.json`.
3. `versions.txt`: A changelog of a dependency package.

Your objectives are:

1. **Semantic Version Extraction**: Parse `versions.txt` to find the lowest stable semantic version (i.e., versions without pre-release tags like `-alpha` or `-beta`) that is greater than or equal to `2.0.0`. Save this exact version string (including the 'v' prefix) into a new file at `/home/user/migration/version.info`.

2. **Code Migration**: Modify `/home/user/migration/migrate.py` so that it is fully compatible with Python 3. Do not change the core schema transformation logic, just fix the Python 2 specific syntax and methods (e.g., dictionary iteration and print statements) so it runs successfully under `python3`. 

3. **Data Processing**: Run the updated `migrate.py` using Python 3 to process `input.json` and generate `/home/user/migration/output.json`. The script takes two positional arguments: the input file path and the output file path.

4. **CI/CD Packaging**: Package the results as a CI/CD build artifact. Create a gzip-compressed tarball named `/home/user/migration/artifact.tar.gz` that contains exactly the following three files at its root (do not include the parent directory structure in the archive):
   - `version.info`
   - `migrate.py`
   - `output.json`

Ensure all output files have exactly the names specified above.