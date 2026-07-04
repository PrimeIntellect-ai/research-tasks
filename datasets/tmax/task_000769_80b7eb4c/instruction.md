You are an AI assistant helping a technical writer organize and extract configurations from a set of fragmented, periodically rotated documentation archives. 

The writer has several documentation archives located in `/home/user/docs_raw/`. These archives (`part1.tar.gz` and `part2.tar.gz`) contain Markdown files with embedded configuration parameters. Furthermore, an automated process has stamped these Markdown files with draft watermarks that must be removed.

Your task consists of the following phases:

1. **Extraction and Text Transformation:**
   - Extract all `.tar.gz` files found in `/home/user/docs_raw/` into a new directory `/home/user/docs_cleaned/`.
   - Using standard Linux text transformation tools (like `sed` or `awk`), find and remove all instances of the draft watermark from all the extracted Markdown (`.md`) files. The watermark follows the exact regex pattern: `\[DRAFT_WATERMARK_[0-9]+\]`. Ensure the watermarks are completely removed (replace with an empty string) and save the changes in the files.

2. **Configuration Interpretation & Code Writing (Go):**
   - There is a configuration file located at `/home/user/doc_rules.ini` that defines how to extract API configuration blocks from the documentation.
   - Write a Go program at `/home/user/extractor.go` that reads `/home/user/doc_rules.ini` to determine the `start_marker` and `end_marker` for configuration blocks.
   - The Go program must iterate through all `.md` files in `/home/user/docs_cleaned/`, look for lines between the `start_marker` and `end_marker` (exclusive of the markers themselves), and parse the key-value pairs within those blocks (which are formatted as `key: value`).
   - The Go program must convert these key-value pairs into a single combined JSON object and write it to `/home/user/compiled_config.json`. If multiple files have different keys, combine them into one flat JSON object. (You can assume keys are unique across all docs).

3. **Archive Creation:**
   - Compress the cleaned Markdown files (from `/home/user/docs_cleaned/`) and the generated `/home/user/compiled_config.json` into a single zip file located at `/home/user/final_docs.zip`.
   - The zip file should contain the `.md` files and `.json` file at its root (do not include the parent directory structure).

Constraints:
- Use Go to perform the block extraction and JSON conversion.
- Ensure the resulting JSON in `/home/user/compiled_config.json` is properly formatted and valid.