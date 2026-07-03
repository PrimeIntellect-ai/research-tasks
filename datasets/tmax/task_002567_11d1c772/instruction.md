You are an artifact manager tasked with curating a large binary repository. 

Due to a bug in a legacy log rotation script that wrote concurrently with the artifact ingester, the metadata files for our repository have been slightly corrupted and inconsistently formatted. 

Navigate to the repository directory located at `/home/user/artifact_repo`. Inside, you will find a deeply nested directory structure containing several metadata files ending with the `.info` extension.

Your task is to consolidate the information from all these `.info` files into a single, clean CSV index file. 

However, you must handle the following issues:
1. **Null Bytes:** Many `.info` files contain random null bytes (`\x00`) mixed into the text due to the concurrent write bug. You must strip these out before parsing.
2. **Inconsistent Casing:** The keys in the text files are formatted as `Key: Value`, but the casing is inconsistent (e.g., `Id:`, `ID:`, `id:`, `Version:`, `VER:`, `version:`, `Size:`, `size:`, `SIZE:`).
3. **Line Endings:** Some files have Windows (`\r\n`) line endings, while others have Linux (`\n`) line endings.

**Requirements:**
- Extract the `id`, `version`, and `size` values from every `.info` file in the repository.
- Create a compiled CSV file at `/home/user/registry_index.csv`.
- The CSV must have exactly this header as the first line: `id,version,size`
- The following lines must contain the extracted data for each artifact, separated by commas.
- Sort the data rows (excluding the header) by the `size` column in **descending numerical order**. If sizes are identical, sort alphabetically by `id`.

Use Bash, `awk`, `sed`, `find`, or similar terminal tools to accomplish this task.