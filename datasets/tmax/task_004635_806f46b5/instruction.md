We have a legacy configuration management system that stores backups as nested archives. We need to apply a global configuration update to thousands of configuration files based on a printed memo, and then repackage the archive as efficiently as possible.

Here are the requirements:
1. There is an image of the global configuration overrides located at `/app/config_schematic.png`. Use OCR (e.g., `pytesseract`) to extract the text from this image. You are looking for two key-value pairs: `MAX_CONNECTIONS` and `TIMEOUT`.
2. There is a nested archive at `/app/configs.tar.gz`. Inside this tarball are multiple `.zip` files, and inside those zip files are `.conf` text files.
3. Write a Python script at `/app/update_configs.py` that streams or memory-maps through `/app/configs.tar.gz`, unpacks the nested zip files in memory, and reads the `.conf` files.
4. For every `.conf` file, if the keys `MAX_CONNECTIONS` or `TIMEOUT` exist, update their values to the ones extracted from the image. If they don't exist, append them to the end of the file.
5. Repackage the updated `.conf` files into their respective `.zip` files, and bundle those updated zip files into a single output archive at `/app/updated_configs.tar.xz`.
6. You must apply maximum LZMA compression to the output archive so that its file size is minimized. Our strict storage limit requires the final `/app/updated_configs.tar.xz` to be under a specific size threshold (you should aim for the smallest possible size using maximum compression settings).

Run your script to generate `/app/updated_configs.tar.xz`. The verification suite will check if the configuration values inside the archive match the image, and if the final archive size meets our rigorous threshold.