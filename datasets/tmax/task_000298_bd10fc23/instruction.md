You are an AI assistant helping a technical writer organize a messy export of documentation assets.

The writer has a directory of raw files at `/home/user/docs_raw`. Many of the files have incorrect or missing extensions. You need to identify all the actual PNG image files, move them to a designated folder, and create a manifest.

Here are your instructions:
1. Parse the configuration file located at `/home/user/doc_config.ini`. Look for the `[Paths]` section and extract the value of `image_dir`. This is your destination directory. If the destination directory does not exist, create it.
2. Search recursively through `/home/user/docs_raw` for all files that are *actually* PNG images. You must determine this by reading the file's binary header (magic number), not by looking at the file extension. Some files named `.png` might be text files, and some text or data files might actually be PNGs.
3. Move all genuine PNG files you find into the destination directory. 
4. When moving, ensure the destination filename ends with `.png`. If the original filename already ends in `.png`, keep the name exactly the same. If it does not end in `.png`, append `.png` to the original filename (e.g., `diagram.dat` becomes `diagram.dat.png`). Do not overwrite files; you can assume base names are unique.
5. Finally, write a log file at `/home/user/png_manifest.txt`. This file should contain the absolute paths of all the PNG files you successfully moved to the destination directory, one path per line, sorted alphabetically.

Use Python or bash utilities to accomplish this.