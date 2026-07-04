You are a data scientist preparing a text corpus for a custom NLP model. You need to build a robust data preprocessing pipeline entirely using standard Linux utilities and Bash.

You have a dataset containing metadata and raw text files:
- Metadata file: `/home/user/data/metadata.tsv` (Tab-separated, columns: `doc_id`, `year`, `category`)
- Raw text documents: Directory `/home/user/data/docs/` containing files named `<doc_id>.txt`
- Stopwords list: `/home/user/data/stopwords.txt` (One word per line)

Your objective is to write a Bash script at `/home/user/process_data.sh` that performs the following pipeline, and then execute it:

1. **Multi-source Data Joining:** Iterate through the entries in `metadata.tsv`. If a corresponding text file exists in the `docs` directory, process it. If it does not exist, skip it.
2. **Tokenization and Cleaning:**
   - Convert all text in the document to lowercase.
   - Replace any character that is NOT an English letter (`a-z`), a digit (`0-9`), or whitespace with a single space.
   - Tokenize the text by splitting on any whitespace (so each valid alphanumeric sequence becomes a separate token).
   - Filter out any token that appears in the `stopwords.txt` file (exact match).
   - Remove any empty tokens or tokens consisting only of spaces.
3. **Large-scale Data Storage Management:**
   - For each processed document, save the cleaned tokens (one token per line) into a partitioned directory structure based on its metadata: `/home/user/processed/<year>/<category>/<doc_id>.tok`. Create the directories if they don't exist.
4. **Summary Generation:**
   - After processing all files, generate a summary manifest file at `/home/user/manifest.csv`.
   - The format must be exactly: `doc_id,year,category,token_count`
   - The file must be sorted alphabetically by `doc_id`.
   - Do not include headers in the CSV.

Run your script to produce the final `/home/user/processed/` directory and the `/home/user/manifest.csv` file. Ensure your script has executable permissions.