You are helping me organize some messy project files received from an international collaborator. The files are delivered in an archive at `/home/user/incoming_project.tar.gz`.

Please perform the following operations:
1. Extract `/home/user/incoming_project.tar.gz` into a new directory called `/home/user/project_workspace`.
2. The collaborator used a legacy text encoding. Find all `.txt` files in the extracted directory and convert their encoding from `ISO-8859-1` to `UTF-8`. Save the converted files in-place (overwrite the original `.txt` files).
3. The project contains some duplicate files. Find files with exactly identical content. Keep the file that comes first alphabetically by its full path, and replace any other identical files with a hard link to the first one.
4. Generate a manifest file at `/home/user/manifest.sha256`. It should contain the SHA256 checksums of all files inside `/home/user/project_workspace`. The manifest format should be standard `sha256sum` output (hash followed by two spaces and the relative file path like `./docs/file.txt`). Run this from inside `/home/user/project_workspace` so the paths are relative. Sort the manifest alphabetically by the file path.
5. Finally, package the cleaned and deduplicated workspace into a new gzip-compressed tar archive at `/home/user/clean_project.tar.gz`. The root of the archive should be the contents of the workspace (i.e., extracting it should not create an extra `project_workspace` top-level directory).

Let me know when you have completed all steps.