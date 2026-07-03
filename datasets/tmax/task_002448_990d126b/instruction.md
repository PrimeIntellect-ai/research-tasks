I need help organizing and sanitizing some project log files before we back them up. 

There are several log files in `/home/user/logs/`.
I've left an image containing the sanitization instructions at `/app/instructions.png`. 

Please do the following:
1. Extract the text from `/app/instructions.png` (you can use `tesseract`). It contains three fields: `TARGET`, `REPLACE`, and `PREFIX`.
2. For every `.log` file in `/home/user/logs/`, replace all occurrences of the `TARGET` string with the `REPLACE` string.
3. Rename all the modified `.log` files by prepending the `PREFIX` to their original filenames (e.g., if PREFIX is `ok_`, `app.log` becomes `ok_app.log`).
4. Archive all the renamed log files into a single compressed tarball named `archive.tar.gz` in `/home/user/logs/`. You must use the maximum possible gzip compression level to save space.
5. Create a symbolic link at `/home/user/latest_archive` that points to `/home/user/logs/archive.tar.gz`.

Ensure the final compressed archive size is as small as possible. The automated verifier will check the size of your archive.