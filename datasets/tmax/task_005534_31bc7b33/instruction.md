You are a data scientist tasked with cleaning and stratifying a messy dataset of text files. 
You have been given a directory of raw text files at `/home/user/raw_data/`. These files were scraped from various older web forums and have mixed character encodings (some are UTF-8, while others are ISO-8859-1 or Windows-1252). 

Your goal is to write a Python script at `/home/user/clean_data.py` that processes these files, normalizes the text, stratifies them into two categories, and outputs a sampled dataset.

Here are the exact requirements for your script:

1. **Read and Decode**: Process every `.txt` file in `/home/user/raw_data/`. Since the encodings are mixed, your script should first attempt to read each file as `utf-8`. If a `UnicodeDecodeError` occurs, fallback to reading it as `iso-8859-1`.

2. **Tokenization and Normalization**:
   - Convert the entire text of the file to lowercase.
   - Replace any character that is NOT an English lowercase letter (`a-z`), a digit (`0-9`), or a space (` `) with a single space.
   - Split the resulting string by spaces to create a list of tokens. Remove any empty string tokens.

3. **Stratification**:
   - Categorize each document into one of two categories: `tech` or `other`.
   - A document is categorized as `tech` if its normalized token list contains the exact token `python` or the exact token `linux`.
   - Otherwise, it is categorized as `other`.

4. **Sampling**:
   - For each category (`tech` and `other`), collect the filenames that belong to it.
   - Sort the filenames alphabetically in ascending order.
   - Select the first 3 files from each sorted category list to form your stratified sample.

5. **Output**:
   - Save the sampled data to a JSON file at `/home/user/processed_sample.json`.
   - The JSON structure must be a dictionary with two keys: `"tech"` and `"other"`.
   - The value for each category should be a dictionary mapping the filename (e.g., `"data01.txt"`) to its corresponding list of normalized tokens.

Run your script to generate the output file.