You are helping a researcher organize and salvage a messy dataset directory located at `/home/user/research_data`. The researcher attempted to create a backup script earlier, but it accidentally created a recursive symlink loop inside the directory, and the dataset contains mixed encodings, corrupted archives, and incorrectly named binary files.

Your task is to write and execute bash commands/scripts to clean and extract the data based on the following requirements:

1. **Avoid Infinite Loops:** Navigate the `/home/user/research_data` directory safely. There is at least one symlink that points back to a parent directory, which will cause infinite recursion if followed blindly.
2. **Binary Header Extraction:** Find all files with the `.dat` extension that are actually PNG images (you must verify this by checking for the PNG magic bytes/header). Copy these valid PNG files to `/home/user/recovered_pngs/` and change their extension to `.png` (keep their original base filename).
3. **Character Encoding Conversion & Metadata Search:** Find all `.csv` files within the dataset that were modified in the last 2 days. These files are currently encoded in `WINDOWS-1252`. Convert their encoding to `UTF-8` and save the converted files into `/home/user/clean_csvs/` (keep their original filenames).
4. **Archive Integrity Verification:** The dataset contains several `.tar.gz` archives. Test their integrity. Write the absolute paths of all *corrupted* or *invalid* `.tar.gz` files to `/home/user/bad_archives.log`, with one path per line.

Ensure that the output directories (`/home/user/recovered_pngs/` and `/home/user/clean_csvs/`) are created before copying files into them. Do not include files accessed via the infinite symlink loop multiple times.