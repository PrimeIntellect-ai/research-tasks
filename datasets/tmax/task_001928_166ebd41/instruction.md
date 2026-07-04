You are tasked with helping a developer migrate a legacy data processing pipeline from Python 2 to Python 3. The pipeline handles data files with mixed character encodings, sorts and merges them, and verifies the output. You also need to set up a basic CI pipeline configuration.

Here is the current state of the workspace `/home/user`:
1. `legacy_processor.py`: A Python 2 script that reads a file, strips quotes, and prints the lines. It currently fails in Python 3 due to `print` syntax, binary/string mixing, and missing encoding handling.
2. `data_utf8.csv`: A data file encoded in UTF-8.
3. `data_cp1252.csv`: A data file encoded in CP-1252.
4. `data_utf16.csv`: A data file encoded in UTF-16-LE.
5. `baseline.csv`: The expected final merged and sorted output.

Your objectives:

1. **Migrate the Python Script**: Create a new script `/home/user/processor.py` compatible with Python 3.
   - It must take exactly two command-line arguments: `filepath` and `encoding`.
   - It should read the file using the specified encoding.
   - It should strip any double quotes (`"`) and whitespace from each line.
   - It should print each cleaned line to standard output.

2. **Create the Shell Pipeline**: Write a bash script `/home/user/pipeline.sh` that does the following:
   - Executes `processor.py` on `data_utf8.csv` (encoding: `utf-8`), `data_cp1252.csv` (encoding: `cp1252`), and `data_utf16.csv` (encoding: `utf-16le`).
   - Merges the standard output of all three executions.
   - Sorts the merged output numerically by the second column (comma-separated).
   - Saves the sorted output to `/home/user/merged.csv`.
   - Diffs `/home/user/merged.csv` against `/home/user/baseline.csv` and saves the output of the diff command to `/home/user/diff_report.txt`.

3. **Set up a CI Pipeline**: 
   - Create a GitHub Actions workflow file at `/home/user/.github/workflows/data_pipeline.yml`.
   - The workflow should trigger on `push` to the `main` branch.
   - It should have a single job named `test-pipeline` running on `ubuntu-latest`.
   - The steps should include checking out the code, setting up Python 3.9, running `bash pipeline.sh`, and failing if `/home/user/diff_report.txt` is not empty (you can use a simple bash conditional for this step).

Ensure your bash script `pipeline.sh` is executable.