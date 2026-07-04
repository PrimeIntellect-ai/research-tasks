You are helping a technical writer organize a messy archive of compressed documentation drafts. 

In the directory `/home/user/drafts/`, there are several gzipped text files named `draft_001.txt.gz`, `draft_002.txt.gz`, and so on. These files are quite large, so you should avoid fully extracting them to disk or loading entire files into memory at once.

Your task is to organize these files using a Python script. Specifically, you need to:
1. Read each compressed file via a streaming approach (e.g., using Python's `gzip` module reading line-by-line).
2. Scan the early lines of each file to find a specific metadata line that starts exactly with `TITLE: ` (e.g., `TITLE: API Reference v2`).
3. Extract this title and convert it to a "slug" to use as the new filename. To create the slug: convert to lowercase, replace all spaces with underscores (`_`), and remove any characters that are not alphanumeric or underscores.
4. Rename the original gzipped file and move it to the directory `/home/user/final_docs/` using the slug as the new name (e.g., `api_reference_v2.txt.gz`).
5. Your script must print a mapping of the renames to standard output in the exact format: `[original_filename] -> [new_filename]` (e.g., `draft_001.txt.gz -> api_reference_v2.txt.gz`).
6. Run your Python script and use standard stream redirection (bash piping/redirection) to save this standard output to a log file at `/home/user/rename.log`. The output in the log file must be sorted alphabetically by the original filename.

Make sure the `/home/user/final_docs/` directory is created if it doesn't exist.