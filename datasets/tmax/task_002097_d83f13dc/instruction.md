You are helping a developer organize a messy project dump. 

You have been given an archive located at `/home/user/workspace/incoming.tar.gz`. 

Please perform the following operations using standard Linux command-line tools:
1. Extract the contents of `/home/user/workspace/incoming.tar.gz` into a new directory: `/home/user/workspace/extracted/`.
2. Search through the extracted files and identify any files that are compiled ELF binaries. Move all identified ELF files into a new directory called `/home/user/workspace/binaries/` (do not recreate the original subdirectory structure for these files, just place them directly in `binaries/`).
3. Find all `.csv` files within the `extracted/` directory (including subdirectories) that are currently encoded in `ISO-8859-1`. Convert their character encoding to `UTF-8`. Replace the original files with the UTF-8 converted versions (keep the exact same filenames and locations).
4. Among the remaining files in the `extracted/` directory, locate a file named `metadata.json`. Extract the string value associated with the key `"project_version"` and write just that value (e.g., `1.4.2`) to a new file at `/home/user/workspace/version.txt`.
5. Finally, create a zip archive at `/home/user/workspace/cleaned_project.zip` containing all the current contents of the `/home/user/workspace/extracted/` directory (which should now be missing the ELF binaries and have the updated UTF-8 CSV files). The root of the zip archive should contain the contents of the `extracted/` directory, not the `extracted` folder itself.

Ensure all paths are strictly adhered to.