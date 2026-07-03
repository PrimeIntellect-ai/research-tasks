You are a localization engineer at a software company. A recent system migration corrupted several of our translation files, and the internal translation pipeline is currently broken. Your task is to repair the pipeline, fix the corrupted translation encodings, and generate summary statistics. 

Here are the requirements for this task:

**1. Fix the Vendored Package**
We use a vendored version of the `polib` library to parse our `.po` files. It is located at `/app/vendored/polib-1.1.1`. However, a recent erroneous commit introduced a bug into this package: it fails to handle default string encodings correctly when the PO file's charset metadata is malformed or missing, instead falling back to an overly restrictive encoding. 
- Identify the perturbation in `/app/vendored/polib-1.1.1/polib.py`.
- Fix the package so it defaults to `utf-8` instead of the broken fallback.
- Install the fixed package into your Python environment.

**2. Implement a DAG-based Data Pipeline**
Write a Python script at `/home/user/run_pipeline.py` that orchestrates the data processing. Your script must explicitly model the workflow as a Directed Acyclic Graph (DAG) (you can use standard Python structures like dictionaries, `asyncio`, or standard classes to represent and execute the dependencies: Read -> Clean Encodings -> Aggregate -> Save).

**3. Fix Character Encodings**
The input `.po` files are located in `/home/user/raw_locales/` (e.g., `es.po`, `fr.po`, `de.po`). Many of the translated strings (`msgstr`) have "mojibake" corruption because UTF-8 byte sequences were improperly decoded as Latin-1 (ISO-8859-1) during the migration.
- Implement an automated character encoding repair step in your pipeline.
- Specifically, you must programmatically convert the corrupted mojibake strings (e.g., "Ã©") back to their correct UTF-8 representations (e.g., "é").

**4. Aggregate Summary Statistics**
Your pipeline must compute summary statistics across all processed PO files. 
- For each language (determined by the filename, e.g., "es"), calculate:
  - `total_translations`: The number of non-empty `msgstr` entries.
  - `avg_translation_length`: The average character length of the fixed `msgstr` entries (rounded to 2 decimal places).
- Output these statistics to exactly `/home/user/summary.json` in the following format:
  ```json
  {
    "es": { "total_translations": 42, "avg_translation_length": 15.34 },
    "fr": { ... }
  }
  ```

**5. Save the Restored Files**
Save the corrected PO files to `/home/user/fixed_locales/` using the original filenames (e.g., `/home/user/fixed_locales/es.po`).

Complete the script and execute it to ensure `/home/user/summary.json` and the repaired `.po` files are generated. Your solution will be evaluated based on the accuracy of the recovered strings against a hidden golden reference.