You are an AI assistant helping a bioinformatics researcher organize a messy data dump. 

The researcher has an archive located at `/home/user/research_data/raw_dump.tar.gz`. This archive contains a complex, deeply nested directory structure of experimental files (`.dat`) and log files (`.log`).

Your task is to organize this dataset without duplicating large data files on disk, following these exact steps:

1. **Extract**: Extract the contents of `/home/user/research_data/raw_dump.tar.gz` into a new directory at `/home/user/workspace/`.
2. **Filter & Hard Link**: The researcher only wants valid data files. Find all `.dat` files within `/home/user/workspace/` that meet **both** of the following criteria:
   - Modified after `2023-01-01 00:00:00`
   - File size is strictly greater than 10 Kilobytes (10,240 bytes)
   Create **hard links** for all matching files inside a new directory: `/home/user/organized_dataset/data/`. Do not copy the files.
3. **Bulk Rename**: In the `/home/user/organized_dataset/data/` directory, rename all the hard-linked files to a standard sequential format: `subject_001.dat`, `subject_002.dat`, `subject_003.dat`, and so on. The numbering must be assigned based on the alphabetical order of the *original* base filenames (e.g., if the original files were `alpha.dat` and `zeta.dat`, `alpha.dat` becomes `subject_001.dat` and `zeta.dat` becomes `subject_002.dat`).
4. **Symlink Latest Log**: Find the single most recently modified `.log` file anywhere inside `/home/user/workspace/`. Create a **symbolic link** at `/home/user/organized_dataset/latest_run.log` that points to this specific log file.
5. **Archive**: Finally, create a compressed tarball of the organized dataset at `/home/user/clean_dataset.tar.gz`. The archive should contain the `organized_dataset` directory at its root (i.e., extracting it should yield an `organized_dataset/` directory).

Ensure all paths and filenames match these instructions exactly. Work entirely in the terminal using standard Linux tools.