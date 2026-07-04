I am a researcher trying to organize a messy batch of legacy dataset files. The files and logs are scattered in `/home/user/dataset_raw/`. I need you to write a Python script (and use any helpful shell commands) to filter, standardize, and package the successful datasets.

Here are your specific instructions:

1. **Parse the Log File:**
   Read `/home/user/dataset_raw/experiments.log`. This file contains multi-line records of experiment runs, separated by lines containing only `---`. Extract the `Dataset-ID` from every record where the `Status` is exactly `SUCCESS`.

2. **Search for Data Files:**
   Search recursively in `/home/user/dataset_raw/` for all files that meet ALL of the following criteria:
   - The filename contains a successful `Dataset-ID`.
   - The filename ends with `.dat`.
   - The file size is strictly greater than 50 bytes.

3. **Convert File Encodings:**
   The matching data files were saved on different legacy systems and may be encoded in UTF-8, UTF-16, or ISO-8859-1. Read the contents of each valid file, and convert the text to standard `UTF-8`.
   Save these newly encoded UTF-8 files into a new directory: `/home/user/clean_dataset/`. Keep their original basenames (e.g., if you found `data_7392.dat`, save it as `/home/user/clean_dataset/data_7392.dat`).

4. **Generate a Manifest:**
   After converting and moving the files, calculate the SHA-256 checksum of each new UTF-8 file in `/home/user/clean_dataset/`. 
   Write a JSON file to `/home/user/clean_dataset/manifest.json`. The JSON file must contain a single dictionary where the keys are the file basenames (e.g., `"data_7392.dat"`) and the values are their SHA-256 hex digests.

Ensure your script handles everything end-to-end. I only care about the final state of `/home/user/clean_dataset/` and the `manifest.json`.