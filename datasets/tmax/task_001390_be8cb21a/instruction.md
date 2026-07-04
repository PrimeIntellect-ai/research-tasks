You are an AI assistant helping a researcher organize their experimental datasets. The researcher has a batch of compressed archives, but suspects some of them were corrupted during download. You need to process these archives, verify their integrity, extract specific binary file headers, and generate a summary report.

Here are your instructions:
1. Read the configuration file located at `/home/user/dataset_rules.conf`. It contains key=value pairs, specifically `ARCHIVE_DIR` (the path to the directory containing the datasets) and `MAGIC_BYTES_COUNT` (the number of header bytes to extract).
2. Look for all `.tar.gz` files in the directory specified by `ARCHIVE_DIR`.
3. Verify the archive integrity of each `.tar.gz` file. You must skip any archive that is corrupted or invalid.
4. For each valid archive, list its contents and find all files with the `.bin` extension.
5. Extract the first `MAGIC_BYTES_COUNT` bytes from each `.bin` file located inside the valid archives. You must not extract the files to the disk permanently; read them directly from the archive or use temporary pipes.
6. Convert these extracted bytes into a contiguous, lowercase hexadecimal string (e.g., `deadbeef`).
7. Write the results to a log file at `/home/user/magic_summary.txt`.
8. The format for each line in `/home/user/magic_summary.txt` must strictly be: `archive_filename:internal_file_name:hex_string`. (e.g., `data1.tar.gz:experiment.bin:deadbeef`).
9. Sort the final `/home/user/magic_summary.txt` alphabetically.

You may write a bash script or execute terminal commands directly to accomplish this.