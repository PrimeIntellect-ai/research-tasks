You are an AI assistant helping a technical writer organize and modernize a batch of legacy documentation files. 

The writer has provided you with an archive of old files and a configuration mapping. Your task is to extract, convert, and re-package the documentation according to specific rules.

Here is the setup:
- A directory exists at `/home/user/workspace/`.
- Inside this directory, there is an archive named `/home/user/workspace/legacy_docs.tar.gz` containing the old documentation files.
- There is also a configuration file at `/home/user/workspace/mapping.json`.

Your instructions:
1. Extract `legacy_docs.tar.gz` into a new directory `/home/user/workspace/extracted/`.
2. Read the `mapping.json` file. It contains a JSON object where the keys are the original filenames (found in the extracted archive) and the values are objects with instructions for processing each file. The instruction objects contain:
   - `target_name`: The new filename for the output.
   - `encoding`: The original character encoding of the file. You must ensure the final output is encoded in UTF-8.
   - `action`: The transformation to apply to the file's contents.
3. Apply the transformations defined by `action`:
   - If `action` is `"csv_to_json"`: Read the CSV file, convert it to a JSON array of objects (where keys are the column headers from the first row), and save it.
   - If `action` is `"extract_xml_content"`: Parse the XML file and extract the inner text of all `<content>` tags. Join the extracted text with a single newline character (`\n`) and save it as a plain text file.
4. Save the transformed, UTF-8 encoded files into a new directory at `/home/user/workspace/processed/`, using their respective `target_name`s.
5. Finally, create a standard ZIP archive at `/home/user/workspace/clean_docs.zip` that contains only the transformed files (do not include the `processed/` parent directory structure in the zip, just the files themselves at the root of the archive).

You may use Python, shell tools, or any combination of available utilities to complete this task.