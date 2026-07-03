You are a data analyst troubleshooting a broken data pipeline. 

In `/home/user/data_pipeline`, there is a file called `data.tsv` containing tab-separated data (columns: `id`, `category`, `description`). 
There is also a bash script named `process.sh` that is supposed to extract the descriptions (column 3), tokenize them into words, calculate the word frequencies across all descriptions, and output the top 5 most frequent words.

However, just like a plotting script that silently produces blank images due to a backend misconfiguration, `process.sh` is failing silently. Due to a regex/transformation misconfiguration in the pipeline, it outputs blank lines or garbage instead of the actual words.

Your task:
1. Fix `process.sh` so that it correctly processes `data.tsv`. 
   - Skip the header row.
   - Extract only the `description` column.
   - Tokenize the text: convert to lowercase, extract only alphabetical words (a-z) ignoring numbers and punctuation.
   - Count word frequencies.
   - Sort the results by frequency descending. Break any ties by sorting the words alphabetically ascending.
   - Save exactly the top 5 results to `/home/user/data_pipeline/top_words.txt`.
   - The format in `top_words.txt` must be strictly `[count] [word]` separated by a single space, with no leading spaces. (e.g., `5 the`).
2. Run your fixed `process.sh` to generate `/home/user/data_pipeline/top_words.txt`.
3. Create a reproducibility test script at `/home/user/data_pipeline/verify.sh`. This script should:
   - Check that `top_words.txt` contains exactly 5 lines.
   - Verify the contents are correct (you can use a checksum or exact string matching).
   - Exit with code 0 if the output is perfectly accurate, and exit with code 1 otherwise.

All work must be done using Bash shell commands and scripts. Do not use Python, Perl, or other scripting languages.