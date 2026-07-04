You are an MLOps engineer tasked with building a lightweight ETL pipeline to process raw system logs, extract engineered text features, and track the resulting artifacts using standard shell utilities.

Your task consists of two parts: building a Python data processing script and creating an artifact tracking manifest using bash.

**Part 1: ETL Pipeline & Feature Engineering (Python)**
Write a Python script at `/home/user/process_data.py` that does the following:
1. Reads all `.log` files from the directory `/home/user/raw_logs/` (this directory and its contents already exist).
2. For each file, reads the content and tokenizes the text. Tokenization must strictly be defined as: extracting all contiguous sequences of alphanumeric characters (using the regex `[a-zA-Z0-9]+`) and converting them to lowercase.
3. Engineers the following features for each file:
    * `doc_id`: the base name of the file (e.g., `server1.log`).
    * `token_count`: the total number of tokens found in the file.
    * `vocab_size`: the number of *unique* tokens in the file.
    * `error_freq`: the absolute count of the token exactly matching `"error"`.
4. Saves these features into a CSV file at `/home/user/features.csv`.
    * The CSV must have exactly this header: `doc_id,token_count,vocab_size,error_freq`
    * The rows must be sorted alphabetically by `doc_id`.

**Part 2: Artifact Tracking Manifest (Bash)**
After running your Python script to generate `/home/user/features.csv`, you must track the raw inputs and the engineered artifact.
Use standard Linux CLI tools to generate a manifest file at `/home/user/manifest.tsv`.
1. The manifest must contain entries for every `.log` file in `/home/user/raw_logs/` AND the generated `/home/user/features.csv` file.
2. The format of each line must be exactly: `<SHA256_HASH>\t<FULL_FILE_PATH>` (where `\t` is a single tab character). Note that `sha256sum` output often contains two spaces, you must format it to have exactly one tab between the hash and the path.
3. The lines in `manifest.tsv` must be sorted alphabetically by the `<FULL_FILE_PATH>`.

Run your Python script and shell commands to leave the system in the requested final state (`features.csv` and `manifest.tsv` created and correctly formatted).