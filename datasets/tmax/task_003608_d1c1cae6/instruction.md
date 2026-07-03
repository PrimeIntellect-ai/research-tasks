You are a backup administrator tasked with archiving application data. The application stores configuration and record files in `/home/user/app_data/`. These files are in a mix of CSV, XML, and JSON formats.

Your objective is to perform an incremental backup of the data, transforming all modified files into a unified JSON format before archiving them.

Here are your specific instructions:
1. **Identify Incremental Files**: Find all files in `/home/user/app_data/` (and its subdirectories) that were modified *after* the reference file `/home/user/last_backup.stamp`.
2. **Format Conversion**: For each identified file:
   - If it is a CSV file, convert it to a JSON array of objects. (Assume the first row is the header).
   - If it is an XML file, convert it to a JSON array of objects. The XML root element is `<records>`, and each item is wrapped in a `<record>` tag. Its child elements represent the keys and values.
   - If it is already a JSON file, leave its content as-is (but copy it to the staging area).
   - *Requirement*: All transformed files must be saved to `/home/user/backup_staging/` with the exact same base name, but with a `.json` extension. All values in the resulting JSON should be represented as strings.
3. **Archive Creation**: Create a gzip-compressed tarball named `/home/user/incremental_backup.tar.gz` containing all the `.json` files from `/home/user/backup_staging/`. Do not include the `backup_staging` directory structure itself in the archive (i.e., the files should be at the root of the tarball).
4. **Manifest Generation**: Create a manifest file at `/home/user/backup_manifest.json` containing a single JSON array of the absolute paths of the original files from `/home/user/app_data/` that were included in this incremental backup.

You may write scripts in any language (e.g., Python, Node.js) and use standard Linux command-line tools to accomplish this. Ensure all necessary dependencies (like XML parsers if needed) are installed locally or available in the environment.