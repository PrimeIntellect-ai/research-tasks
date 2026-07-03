You are an archiving administrator. We have a legacy data directory that needs to be backed up using a custom script. Our file system has a notoriously messy structure, including symlinks that sometimes form infinite loops.

Your task is to create and run a backup tool that reads a configuration file, traverses the source directory, converts file encodings, applies a custom "compression" (transformation), and writes the output to a backup destination.

Here are the specific requirements:

1. **Configuration File**: 
   Read `/home/user/backup_config.json`. It contains:
   - `source_dir`: The directory to back up (`/home/user/source_data`).
   - `dest_dir`: The destination directory (`/home/user/backup_dest`).
   - `encodings`: A mapping of file extensions to their current character encodings.
   - `compression_key`: A single character used for the custom compression phase.

2. **Directory Traversal & Symlink Loops**:
   - Recursively traverse the `source_dir`.
   - You MUST follow symlinks.
   - You MUST detect infinite symlink loops. If a symlink points to a directory that is an ancestor of the symlink (creating a loop), do not follow it.
   - Log the absolute paths of any detected infinite symlinks (one per line) to `/home/user/symlink_loops.log`.

3. **Encoding Conversion**:
   - For every regular file encountered, read it using the encoding specified in the configuration file for its extension.
   - Convert the text to UTF-8.

4. **Custom "Compression"**:
   - After converting a file's content to UTF-8, apply a custom transformation: XOR every byte of the UTF-8 string with the `compression_key` (provided in the JSON config) and then Base64 encode the resulting byte array.
   - Save this Base64 string to the destination directory.

5. **Destination Structure**:
   - Maintain the original directory structure inside `dest_dir`.
   - Add `.bak` to the end of every backed-up file's name (e.g., `data.csv` becomes `data.csv.bak`).

6. **Manifest**:
   - Create a manifest file at `/home/user/backup_manifest.csv`.
   - It must contain two columns: `original_path,base64_length` (the absolute path of the original file, and the character length of its final Base64 string).

Create the script in whatever language you prefer (Python is recommended), ensure it works, and run it to produce the final `backup_dest` directory, the `symlink_loops.log`, and the `backup_manifest.csv`.