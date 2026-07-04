You are an AI assistant helping a technical writer organize a batch of legacy documentation.

The writer has provided an archive located at `/home/user/legacy_docs.zip`. This archive contains several documentation files in various formats and character encodings, as well as some nested archives left behind by previous team members. Unfortunately, some of the nested archives are corrupted, and the text files use a messy mix of encodings (like Windows-1252, ISO-8859-1, and UTF-16). 

Your objective is to standardize these documents using Python and shell commands. Please follow these steps exactly:

1. **Extract and Verify**: Extract `/home/user/legacy_docs.zip`. Find all nested archives (`.zip`, `.tar.gz`) within the extracted contents. Check their integrity. Ignore any corrupted archives. Extract the contents of all valid nested archives.
2. **Standardize Encodings**: Find all extracted `.txt` and `.csv` files (including those from valid nested archives). Read them in their original encodings and convert their text to standard **UTF-8**. 
3. **Format Conversion**: Convert any `.csv` files into Markdown files (`.md`). The Markdown file should format the CSV data as a standard Markdown pipe table. For example, a CSV row `Name,Age` should become `| Name | Age |` with a separator `|---|---|` after the header. Name the output file exactly the same as the original, but with a `.md` extension. Delete the original `.csv` files after conversion.
4. **Package Cleaned Documents**: Gather all the resulting UTF-8 `.txt` and `.md` files. Place them into a flat directory structure (no subdirectories) and create a new compressed archive at `/home/user/clean_docs.tar.gz`.
5. **Logging**: Create a log file at `/home/user/processing.log` with the following format:
   ```
   CORRUPT_ARCHIVES: <comma-separated list of corrupt archive filenames, e.g., bad.zip>
   PROCESSED_FILES: <comma-separated list of final files in the clean archive, sorted alphabetically, e.g., data.md, intro.txt>
   ```

Constraints:
- You must write a Python script to handle the encoding conversion and CSV-to-Markdown formatting.
- The final archive `/home/user/clean_docs.tar.gz` must only contain the cleaned `.txt` and `.md` files.