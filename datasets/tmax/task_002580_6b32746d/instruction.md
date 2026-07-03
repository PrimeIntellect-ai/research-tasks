You are acting as a backup administrator. We recently received a backup archive containing important financial records, located at `/home/user/backups/financial_records.zip`. Your task is to process this archive, convert the data format, and prepare a new verified backup.

Please perform the following steps:
1. Verify the integrity of the `financial_records.zip` archive. 
2. Extract the contents of the archive into the `/home/user/processing/` directory.
3. The archive contains several `.csv` files. You must convert each `.csv` file into a `.json` file in the same directory. The JSON file should contain a list of objects, where the keys are the CSV column headers and the values are the corresponding row data. The new files should have the same base name but with a `.json` extension.
4. Generate a manifest file named `manifest.sha256` inside `/home/user/processing/`. This file must contain the SHA-256 checksums of all the newly created `.json` files. The format for each line must be `CHECKSUM  filename.json` (two spaces between checksum and filename).
5. Create a new gzip-compressed tar archive at `/home/user/backups/financial_records_converted.tar.gz`. This archive must contain only the newly created `.json` files and the `manifest.sha256` file. The files must be at the root of the archive (do not include the `processing` directory or any other folder structure).

You can write a Python script or use shell commands to complete this task.