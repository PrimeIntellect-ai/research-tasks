You are an AI assistant helping a researcher clean up a messy dataset directory structure. The researcher has been aggregating data, but a faulty backup script introduced some infinite symlink loops, corrupted archives, and inconsistent file formats. 

Your objective is to clean and organize the dataset strictly using Bash commands and standard Linux utilities.

Here are the requirements:

1. **Working Directories**:
   - Source directory: `/home/user/raw_dataset`
   - Destination directory for cleaned data: `/home/user/clean_dataset`
   - Destination directory for corrupt archives: `/home/user/corrupt_archives`
   Create the destination directories before starting.

2. **Handle Symlink Loops**:
   - The `/home/user/raw_dataset` directory contains symlinks. Some of these form infinite recursive loops (which act as broken links).
   - Find and delete all broken/recursive symlinks in `/home/user/raw_dataset` and its subdirectories. Leave valid symlinks intact.

3. **Archive Integrity Verification**:
   - There are `.tar.gz` and `.zip` files scattered in `/home/user/raw_dataset`.
   - Verify the integrity of each archive.
   - For `.zip` files, use `unzip -t`. For `.tar.gz` files, test if they can be successfully read/listed (e.g., using `tar -tzf`).
   - If an archive is corrupt (fails the integrity check), MOVE it to `/home/user/corrupt_archives/`. Leave intact archives where they are.

4. **Format Conversion**:
   - Find all `.json` files in `/home/user/raw_dataset` (and subdirectories). 
   - Each JSON file contains a simple array of objects with exactly two keys: `id` and `value` (e.g., `[{"id": 1, "value": "A"}, ...]`).
   - Convert each `.json` file into a CSV format with the header `id,value` followed by the data rows.
   - Save the converted files in the same directory as the original JSON file, with the exact same base name but a `.csv` extension. (You may use `jq` to parse the JSON).

5. **Hard Link Consolidation**:
   - After conversion, find ALL `.csv` files in `/home/user/raw_dataset` (both pre-existing ones and the newly converted ones).
   - Create hard links for all these `.csv` files into the single flat directory `/home/user/clean_dataset/`.
   - To avoid filename collisions, name the hard link using the format: `<parent_directory_name>_<filename.csv>`. 
     - *Example:* If the file is `/home/user/raw_dataset/experiment_1/results.csv`, the hard link should be `/home/user/clean_dataset/experiment_1_results.csv`.
     - *Example:* If the file is `/home/user/raw_dataset/main.csv`, the hard link should be `/home/user/clean_dataset/raw_dataset_main.csv`.

6. **Verification Log**:
   - Once all operations are complete, generate a sorted manifest of the cleaned dataset.
   - Run `ls -1 /home/user/clean_dataset | sort > /home/user/clean_dataset_manifest.txt`.

Ensure your operations accurately process the files without deleting valid data.