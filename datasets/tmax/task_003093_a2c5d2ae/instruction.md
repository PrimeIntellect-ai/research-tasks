You are a localization engineer tasked with updating translations for a new web application. We have a set of raw translation files in a custom `.loc` format located in `/home/user/data/`. 

We use an internal Python package called `locparse` to extract translations from these files. The source code for this package is provided at `/app/locparse`. However, our recent test runs show that it is missing some translation keys due to a bug in the parser. 

Your tasks are to:
1. Identify and fix the bug in the `locparse` package at `/app/locparse`. It currently fails to extract the final translation key in certain blocks. 
2. Write a Python script `/home/user/process_loc.py` that uses `locparse` to read all `.loc` files in `/home/user/data/`.
3. For each `.loc` file (e.g., `es.loc`), extract the translation key-value pairs.
4. Load the JSON template located at `/home/user/template.json`.
5. Generate a populated JSON file for each language in `/home/user/output/` (e.g., `/home/user/output/es.json`). The output JSON must perfectly match the template's structure, replacing the empty string values with the extracted translated strings. If a key from the template is missing in the `.loc` file, leave it as an empty string.
6. Implement pipeline logging: Your script must create a log file at `/home/user/pipeline.log`. For each processed file, write a line in the exact format: `[INFO] Processed <filename>: extracted <count> keys.` (e.g., `[INFO] Processed es.loc: extracted 45 keys.`).

To succeed, the generated JSON files must achieve an accuracy of >= 0.98 compared to the hidden ground truth translation files, measured by the proportion of correctly populated values for the keys present in the template.