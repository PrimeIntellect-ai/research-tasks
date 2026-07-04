You are tasked with writing a Python script to help a configuration manager track and consolidate distributed system settings. 

Over time, our application's configuration files have been fragmented and scattered across a directory tree. We need to parse these files, merge the tracked settings based on versioning, and split the final configuration into manageable chunks.

Here are the requirements:
1. Recursively traverse the directory `/home/user/system_configs/` to find all files with the `.ini` extension.
2. Parse each `.ini` file. Valid configuration files contain two sections: `[Metadata]` and `[Settings]`.
3. In the `[Metadata]` section, check for the key `track_changes`. If `track_changes` is `false` or missing, completely ignore the file.
4. If `track_changes` is `true`, read the `version` integer from the `[Metadata]` section, and extract all key-value pairs from the `[Settings]` section.
5. Merge all extracted `[Settings]` from all valid files into a single master dictionary. 
   - If multiple files define the same setting key, the value from the file with the **highest** `version` number should be kept. (Assume no two valid files have the same version number for this exercise).
6. Once the master dictionary is built, sort it alphabetically by the setting keys.
7. Chunk the sorted master dictionary into multiple JSON files, each containing exactly 2 key-value pairs (the final chunk may have fewer if the total number of keys is odd). 
8. Save these chunks in a new directory `/home/user/settings_chunks/` named as `chunk_1.json`, `chunk_2.json`, etc., following the alphabetical order of the keys.

Create and execute a Python script to perform this exact workflow. Format the output JSON files with 2 spaces for indentation.