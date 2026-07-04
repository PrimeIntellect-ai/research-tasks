You are an artifact manager tasked with safely curating binary repository files. In the directory `/home/user/artifact_repo`, there are several active data artifacts. Some of these files are currently being written to by an active process, indicated by the presence of a corresponding `.lock` file.

Your task is to safely process and archive only the completed (unlocked) artifacts. 

Specifically, you must:
1. Identify all `artifact_*.dat` files that do **not** have a corresponding `artifact_*.lock` file in the same directory.
2. For each completed artifact, there is a corresponding `artifact_*.meta` file containing metadata in a simple `key=value` text format (one pair per line). Convert this metadata into a valid JSON file named `artifact_*.json` (with keys and values as strings).
3. Rename the completed `artifact_*.dat` files by prepending `curated_` to their names (e.g., `artifact_01.dat` becomes `curated_artifact_01.dat`).
4. Create a gzip-compressed tar archive named `/home/user/curated_archive.tar.gz` containing ONLY the renamed `curated_*.dat` files and the newly created `*.json` files. Do not include directory structures (the files should be at the root of the archive).

Do not process or include any files associated with locked artifacts.