You are a backup administrator tasked with creating a custom data archival tool that applies a specific transformation to backup files, generates a manifest checksum, and packages them for storage.

We have an old scanned manual page located at `/app/archival_spec_page.png` that describes the proprietary transformation algorithm we must use for compliance reasons. You will need to extract the text from this image (e.g., using `tesseract`) to understand the algorithm rules. 

Additionally, there is a configuration file at `/app/archival_config.json` that contains specific formatting options for the output file:
```json
{
    "footer_prefix": "MANIFEST_START|",
    "footer_suffix": "|MANIFEST_END",
    "hash_algorithm": "sha256"
}
```

Your task is to write a Python script at `/home/user/archive_tool.py` that can be run from the command line as follows:
`python3 /home/user/archive_tool.py <input_file_path> <output_file_path>`

The script must:
1. Read the binary data from the input file.
2. Apply the byte-level transformation described in `/app/archival_spec_page.png`.
3. Calculate the checksum (using the algorithm specified in the config file) of the **original, un-transformed** binary input data.
4. Write the transformed binary data to the output file.
5. Append the checksum to the end of the output file, wrapped exactly in the `footer_prefix` and `footer_suffix` strings from the configuration file. (e.g., `MANIFEST_START|a1b2c3...|MANIFEST_END`). Keep it as UTF-8 encoded bytes appended directly to the file.

Ensure your code handles binary data properly and correctly interprets the configuration file. The script should use standard libraries where possible, though you can install packages if needed for the setup.