You are acting as a localization engineer. You have been given a legacy translation file that needs to be processed, validated, and sampled for human review.

The input file is located at `/home/user/translations.csv`. However, it has been saved in an older `ISO-8859-1` encoding instead of `UTF-8`.
The file is in a "wide" format with the following columns:
`key,en,fr,de,es`

Your task is to write a single Bash script at `/home/user/process_loc.sh` (make it executable) that performs the following multi-stage pipeline using standard Unix tools (like `iconv`, `awk`, `sort`, etc.):

1. **Character Encoding Handling**: Read the input file `/home/user/translations.csv` and convert its contents from `ISO-8859-1` to `UTF-8`.

2. **Wide-Long Format Reshaping**: Transform the converted CSV data from wide format to long format. The output must be written to `/home/user/long_format.csv` with the header:
`key,locale,translation`
For each key in the input, there should be 4 rows in the long format (for `en`, `fr`, `de`, `es`).

3. **Anomaly Detection**: Compare the character length of each localized translation (`fr`, `de`, `es`) against its corresponding English (`en`) source length. If the localized translation length is strictly less than 0.3 times the English length, OR strictly greater than 3.0 times the English length, flag it as an anomaly. Write these to `/home/user/anomalies.csv` with the header:
`key,locale,en_length,trans_length`
(Do not include `en` in the anomalies).

4. **Data Sampling and Stratification**: Generate a stratified sample for human review. For each locale (`en`, `fr`, `de`, `es`), pick the first 2 keys when sorted alphabetically by `key`. Write this sample to `/home/user/sample.csv` with the header:
`key,locale,translation`
Ensure the file is sorted primarily by `locale` (alphabetically) and secondarily by `key` (alphabetically).

Constraints:
- Only use standard Bash built-ins and coreutils (e.g., `awk`, `sed`, `iconv`, `sort`). Do not use Python, Perl, or other scripting languages.
- You do not need to handle quoted CSV fields containing commas; assume the CSV relies on simple comma delimiters without commas inside the translation strings.
- Ensure your script `/home/user/process_loc.sh` executes the entire pipeline and generates the three required output files. Run your script to produce the outputs before finishing the task.