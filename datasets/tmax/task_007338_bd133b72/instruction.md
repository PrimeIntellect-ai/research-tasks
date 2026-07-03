You are a backup administrator responsible for archiving a legacy international data system. The legacy system stores text files in various outdated character encodings. Before archiving them into a single backup file, you must standardize their encoding to UTF-8 and package them into a proprietary custom archive format.

Your task is to process the directory `/home/user/legacy_data` recursively according to the rules specified in `/home/user/backup.conf`.

Here are the specific requirements:

1. **Configuration Interpretation**: Read `/home/user/backup.conf`. It contains comma-separated values in the format `extension,encoding` (e.g., `txt,ISO-8859-1`). This maps file extensions to their current character encoding.
2. **Directory Traversal & Encoding Conversion**: Recursively find all files in `/home/user/legacy_data` that match the extensions listed in the configuration file. Convert the contents of each matching file from its original encoding to `UTF-8`.
3. **Bulk Renaming**: Save the converted files in the same directory as the original, but insert `.utf8` before the extension (e.g., `report.txt` becomes `report.utf8.txt`).
4. **Custom Compression/Archiving**: Create a single custom archive file at `/home/user/backup.custom` containing all the newly created `*.utf8.*` files. The custom archive format must strictly follow this structure for each file, appended sequentially:
   - A header line: `===FILE:<relative_path>===` (where `<relative_path>` is the file path relative to `/home/user/legacy_data`, e.g., `===FILE:docs/report.utf8.txt===`).
   - The exact `base64` encoded contents of the UTF-8 file (standard base64 output with newlines).
   - A footer line: `===EOF===`

Use standard bash CLI tools (`find`, `iconv`, `base64`, etc.) to complete this task. Do not delete the original files. Ensure the final `backup.custom` file is created correctly.