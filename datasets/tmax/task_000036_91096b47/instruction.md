I need you to help organize a messy directory of project assets located at `/home/user/project_assets`. The files need to be categorized into text and binary files, linked to a new organized structure, and logged in a manifest file using atomic write operations to prevent corruption.

Here are the exact requirements:

1. **File Classification**:
   Read through all the files in `/home/user/project_assets/`. You must classify a file as "binary" if it contains any null bytes (`\x00`) within its first 1024 bytes. Otherwise, classify it as "text".

2. **Linking Strategy**:
   Create a new directory structure under `/home/user/organized/`. Inside it, create two subdirectories: `bin/` and `txt/`.
   - For every **binary** file, create a **hard link** in `/home/user/organized/bin/` keeping the same filename.
   - For every **text** file, create a **symbolic link** (absolute path) in `/home/user/organized/txt/` keeping the same filename.

3. **Atomic Manifest Creation**:
   Generate a JSON manifest file exactly at `/home/user/organized/manifest.json`. 
   To ensure the manifest is never left in a partially written state if the script crashes, you **must** write the JSON data to a temporary file first, and then atomically move/rename it to `/home/user/organized/manifest.json`.
   
   The JSON file should contain a single dictionary mapping the original base filename to an object containing its detected type and its destination link path. 
   Format example:
   ```json
   {
     "file1.ext": {
       "type": "text",
       "link_path": "/home/user/organized/txt/file1.ext"
     },
     "file2.ext": {
       "type": "binary",
       "link_path": "/home/user/organized/bin/file2.ext"
     }
   }
   ```

Write and execute a Python script to perform this exact transformation. Do not delete or modify the original files in `/home/user/project_assets/`.