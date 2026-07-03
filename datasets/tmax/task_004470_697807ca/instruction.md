You are an AI assistant helping a technical writer consolidate and organize a fragmented documentation repository. 

Here is your objective:

1. **Fix and Install the Vendored Sanitizer:**
   There is a local, vendored Python package located at `/app/vendored/text_sanitizer-1.0.0`. This package provides a required text normalization function, but its installation currently fails due to a deliberate perturbation (a syntax error in `text_sanitizer/core.py` and a broken `setup.py`). 
   - Fix the syntax error in `core.py`.
   - Fix the `setup.py` so it correctly identifies the package.
   - Install the package locally in the environment (e.g., `pip install -e /app/vendored/text_sanitizer-1.0.0`).

2. **Extract and Verify Nested Archives:**
   You have a primary archive at `/home/user/raw_docs.tar.gz`. This archive contains several nested archives (zip and tar.gz files). 
   - Extract the contents.
   - Some of the nested archives are deliberately corrupted. You must verify their integrity and only extract from the valid ones, ignoring the corrupt archives.

3. **Parse Structured Data:**
   Inside the valid nested archives, you will find files named `doc_*.json` and `doc_*.xml`. 
   - For JSON files, extract the `content` field.
   - For XML files, extract the text inside the `<Body>` tags.

4. **Transform and Consolidate:**
   - Run the extracted text from each file through the `sanitize_text` function provided by the `text_sanitizer` package.
   - After sanitization, apply a macro/text-editing step: replace all occurrences of the deprecated product name "MacroHard" with "NovaTech".
   - Sort the resulting sanitized strings by their original Document ID (which is the number `*` in `doc_*.json/xml`).
   - Concatenate them into a single Markdown file at `/home/user/final_documentation.md`, with each document's content separated by two blank lines.

Your final output will be evaluated by an automated script that compares `/home/user/final_documentation.md` against a hidden, golden reference using a sequence similarity metric. You must achieve a similarity score of >= 0.98.