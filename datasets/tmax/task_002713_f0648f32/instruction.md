You are a Data Scientist preparing a text dataset for a Natural Language Processing (NLP) model. You need to build a data preparation pipeline using only Bash shell built-ins and standard POSIX command-line utilities (like `awk`, `sed`, `grep`, `join`, `sort`, `tr`, etc.). Do not use Python, Perl, or any other programming languages.

Your pipeline must process two raw data files, join them, enforce a strict schema, and tokenize the text. 

**Input Files:**
1. `/home/user/raw/demographics.txt`
   - Format: Pipe-separated (`|`)
   - Columns: `uid|age|country`
2. `/home/user/raw/reviews.txt`
   - Format: Tab-separated (`\t`)
   - Columns: `uid\treview_text\tscore`

**Processing Requirements:**
1. **Multi-source Data Joining**: Join the two files based on the `uid` column. A user must exist in both files to be included in the output.
2. **Data Schema & Filtering Enforcement**:
   - `age` must be a valid integer greater than or equal to 18.
   - `country` must not be empty.
   - `score` must be an integer strictly greater than 3.
   - `review_text` must not be empty after tokenization.
   - Drop any rows that do not meet these criteria.
3. **Tokenization & Text Cleaning**:
   - Convert `review_text` to strictly lowercase.
   - Remove all characters except letters (a-z), numbers (0-9), and spaces.
   - Replace contiguous spaces with a single dash (`-`).
   - Strip leading and trailing dashes.
   - Example: `"Great product, loved it!"` becomes `"great-product-loved-it"`.

**Output Requirements:**
Create a bash script at `/home/user/build_dataset.sh` that performs this pipeline.
When the script is executed, it must produce an output file at `/home/user/processed/dataset.csv`.
- Format: Comma-separated (`csv`)
- Header row must be exactly: `uid,age,country,tokenized_review`
- Rows must be sorted numerically by `uid` in ascending order.
- Ensure the `/home/user/processed/` directory is created by your script if it doesn't exist.

Execute your script to generate the final `dataset.csv` file.