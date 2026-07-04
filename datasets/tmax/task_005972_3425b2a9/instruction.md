You are tasked with organizing and standardizing a set of disorganized project assets for a new web application build system. The assets are currently stored in `/home/user/project/raw_assets/`.

You need to write and execute a Python script (and use any necessary bash commands) to process these files according to the following strict rules:

1. **Format Conversion**:
   - Convert all image files (`.jpg`, `.jpeg`, `.png`, regardless of case) to WebP format (`.webp`).
   - Convert all JSON files (`.json`, regardless of case) to YAML format (`.yaml`).

2. **Bulk Renaming**:
   - The new filenames must be strictly lowercase.
   - Any spaces (` `) or hyphens (`-`) in the original filename (excluding the extension) must be replaced with underscores (`_`).
   - The extension must be updated to match the new format (`.webp` or `.yaml`).
   - Example: `Hero-Banner 01.PNG` becomes `hero_banner_01.webp`.

3. **Output Directory**:
   - Save all processed files to a new directory: `/home/user/project/processed_assets/`.
   - The original files in `/home/user/project/raw_assets/` must remain unmodified.

4. **Manifest and Checksum Generation**:
   - Generate a CSV manifest file at `/home/user/project/manifest.csv`.
   - The CSV must have the header row exactly as: `processed_filename,original_filename,sha256`
   - Each subsequent row must contain the name of the new processed file, the exact name of the original file, and the SHA256 checksum of the *new processed file*.
   - The rows in the CSV must be sorted alphabetically by the `processed_filename` column.

Constraints:
- Use Python as your primary scripting language. You may need to install external libraries (like `Pillow` for image processing and `PyYAML` for YAML generation) using `pip`.
- Do not hardcode the specific file names in your script; it should dynamically read the `raw_assets` directory.