I am a researcher organizing some messy, archived programming language datasets. I have a directory at `/home/user/research_data/` that contains various archives (`.tar.gz`, `.zip`, `.tar`), some of which are relevant datasets and some of which are just small junk files.

I need you to perform the following data cleaning and extraction tasks:

1. **Filter by Metadata:** Find all archive files (files ending in `.tar.gz`, `.zip`, or `.tar`) inside `/home/user/research_data/` that are strictly **larger than 10 KB** (10240 bytes). Ignore any smaller archives.
2. **Selective Extraction:** From the archives identified in step 1, extract *only* the source code files (`*.py` and `*.js`) into the directory `/home/user/extracted_code/`. You must preserve the directory structure as it exists within the archives.
3. **Format Conversion:** One of the valid archives contains a manifest file named `index.csv`. Extract this file and convert it into a JSON file at `/home/user/extracted_code/index.json`. The JSON should be an array of objects, where the keys are the column headers from the first row of the CSV. (You can use Python/Perl/Awk or any standard CLI tool for this).
4. **Analysis & Redirection:** Calculate the total number of lines across all the extracted `.py` and `.js` files in `/home/user/extracted_code/` combined. Pipe this single integer into a file at `/home/user/loc_summary.txt`.
5. **Re-archiving:** Package the entire `/home/user/extracted_code/` directory (including the new `index.json` and the preserved directory structures) into a new, uncompressed tar archive at `/home/user/clean_dataset.tar`.

Please run the necessary commands in the terminal to accomplish this.