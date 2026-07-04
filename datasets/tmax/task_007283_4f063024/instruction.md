You are an AI assistant helping a data researcher aggregate information from a fragmented dataset. 

The researcher has downloaded a multi-part gzip-compressed tar archive located in `/home/user/archive_parts/`. The files are named `dataset.tar.gz.part_aa`, `dataset.tar.gz.part_ab`, etc. 

Your task is to:
1. Reconstruct the multi-part archive and extract its contents into `/home/user/workspace/`.
2. Inside the extracted contents, you will find a `manifest.csv` file, a `raw/` directory containing CSV data files, and a `links/` directory containing symbolic links to the raw data files.
3. Write a C program at `/home/user/aggregate.c` and compile it to `/home/user/aggregate`. 
4. The C program must:
   - Read the `manifest.csv` file (ignoring the header row `path,description`).
   - For each path listed in the first column of the manifest (which is a relative path like `links/symlink_name.csv` from the `/home/user/workspace/` directory):
     - Check if the symbolic link is valid (unbroken). Skip any broken symbolic links.
     - For valid links, open the target CSV file. These data CSVs have no headers and contain two columns: `sensor_id` (string) and `reading` (integer), separated by a comma.
     - Calculate the total sum of all `reading` values specifically for the `sensor_id` exactly matching `"sensor_a"`.
5. The C program must write the final integer sum to a file located at `/home/user/sensor_a_total.txt`.

Ensure your C code safely handles potentially missing files and properly manages file paths, as the program will be executed from within `/home/user/` (i.e., it should process `/home/user/workspace/manifest.csv` and use appropriate path resolution). Run your compiled C program to generate the final output.