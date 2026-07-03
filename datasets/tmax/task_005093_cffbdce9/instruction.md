You are tasked with investigating a regression in a data processing pipeline and recovering a lost secret from version control.

The repository is located at `/home/user/data_pipeline`. It contains a Python script `process_data.py` that reads a JSON array of floats and applies a softmax transformation. 

Recently, the pipeline started failing when processing data with large variance. You can test it using the provided `large_input.json` file:
`python process_data.py large_input.json`

Currently, on the `master` branch (the latest commit), this script crashes and exits with a non-zero status code due to a numerical instability (a math overflow) that was introduced somewhere in the repository's 200+ commit history. In older commits, the script handles the exact same input successfully.

Additionally, we suspect that a former developer accidentally committed a sensitive API key (which begins with the prefix `DATA_CORP_API_`) in a configuration file somewhere in the git history before realizing the mistake and removing it in a subsequent commit.

Your objectives:
1. Identify the exact Git commit hash that introduced the numerical instability regression. The script `process_data.py` should exit 0 on the commit strictly before it, and exit 1 on the regression commit. (Hint: `git bisect` is highly recommended).
2. Perform forensics on the Git history to recover the leaked API key.
3. Write your findings to a file named `/home/user/debugging_report.txt`.

The `/home/user/debugging_report.txt` file must be formatted exactly as follows:
Line 1: The full 40-character commit hash of the first bad commit that introduced the regression.
Line 2: The exact leaked API key string.

Do not include any other text in the file.