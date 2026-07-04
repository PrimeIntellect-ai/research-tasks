You are an AI assistant helping a climate researcher organize a messy, nested dataset of sensor readings.

The researcher has a directory located at `/home/user/raw_data/` which contains various subdirectories deeply nested by site and date. Scattered throughout these subdirectories are compressed dataset files in either `.tar.gz` or `.zip` format. 

Inside every archive, there is a text file named exactly `metadata.txt`. This file contains several lines of metadata, including a line that specifies the project name, formatted exactly as: `Project: <ProjectName>`.

There is also a configuration file at `/home/user/project_mapping.json` which maps these full project names to standardized 3-letter project codes (e.g., `{"TUNDRA_STUDY": "TUN", "GLACIER_MELT": "GLA"}`).

Your task is to:
1. Traverse the `/home/user/raw_data/` directory to find all `.tar.gz` and `.zip` files.
2. For each archive, read the `metadata.txt` file inside it (without permanently extracting the whole archive to the disk) to find the project name.
3. Look up the project name in `/home/user/project_mapping.json` to get the 3-letter project code. If a project name is not in the JSON file, skip that archive entirely.
4. Copy the valid archives into a new flat directory `/home/user/organized_data/` (you will need to create this directory). When copying, rename the file to prepend the 3-letter project code and an underscore to the original filename. For example, if `sensor_44.zip` belongs to `TUNDRA_STUDY`, it should be copied as `/home/user/organized_data/TUN_sensor_44.zip`.
5. Compress the entire `/home/user/organized_data/` directory into a single archive at `/home/user/final_dataset.tar.gz`.
6. Create a log file at `/home/user/processing_log.txt` where each line records a successful processing event in the exact format:
   `<Original_Full_Path> -> <New_File_Name>`
   Sort the lines in this log file alphabetically by the original full path.

You may write a Python script or use bash commands to accomplish this.