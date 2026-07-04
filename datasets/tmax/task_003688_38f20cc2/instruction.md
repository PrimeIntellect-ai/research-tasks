You are a Data Scientist tasked with building a reproducible data cleaning pipeline using standard Bash utilities. You have received a dataset of model predictions containing text inputs and confidence scores, but it is messy, contains missing values, outliers, and untokenized text.

Your task is to process the raw dataset located at `/home/user/raw_data.tsv` and produce a cleaned dataset at `/home/user/clean_data.txt` following these exact rules:

1. **Format & Separator:** The input file is a tab-separated values (TSV) file with the columns `id`, `text_input`, and `model_score`. The output file must use a pipe character (`|`) as the delimiter.
2. **Header:** Remove the header row.
3. **Missing Value Handling:** Drop any row where `text_input` is completely empty, or exactly the string "NA" or "NaN" (case-sensitive). Drop any row where `model_score` is empty.
4. **Outlier & Model Output Validation:** The `model_score` represents a probability and must be a valid number between `0.0` and `1.0` (inclusive). Drop any row where the score falls outside this range or is not a number.
5. **Tokenization & Normalization:** For the `text_input` column:
    * Convert all text to lowercase.
    * Remove all non-alphanumeric characters (keep only `a-z`, `0-9`, and spaces).
    * Squeeze multiple consecutive spaces into a single space.
    * Trim any leading or trailing spaces from the resulting text.
6. **Output:** The final file `/home/user/clean_data.txt` should have the format `id|tokenized_text|model_score`. 

Please use Bash, standard Unix text processing tools (like `awk`, `sed`, `grep`, `tr`), or Python to complete this pipeline. Ensure the final output file exists and strictly adheres to the requested format.