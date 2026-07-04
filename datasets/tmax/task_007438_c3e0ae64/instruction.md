You are assisting a researcher in organizing a massive influx of experimental datasets. The researcher relies on symbolic and hard links to categorize datasets before archiving them, reducing disk space usage.

Your objective is to build an automated archiving pipeline using Python and standard Linux commands.

Here are your instructions:

1. Create the following directory structure:
   - `/home/user/datasets/raw`
   - `/home/user/datasets/staging`
   - `/home/user/datasets/archives`

2. Create three raw data files in `/home/user/datasets/raw`:
   - `data_A.csv` containing the text "DATA_A"
   - `data_B.csv` containing the text "DATA_B"
   - `data_C.csv` containing the text "DATA_C"

3. Write a Python script at `/home/user/organizer.py` that acts as a directory watcher. The script must do the following continuously (e.g., polling every 1 second):
   - Monitor `/home/user/datasets/staging/` for any symbolic links.
   - For every symbolic link it finds, parse the link's filename. The archive category is the portion of the filename before the first underscore (e.g., a symlink named `neuro_123.sym` belongs to the `neuro` category).
   - Resolve the symbolic link to find the target raw file.
   - Append the target raw file into a compressed tarball (`.tar.gz`) located at `/home/user/datasets/archives/<category>.tar.gz`. The file inside the tarball must have the same name as the original raw file (e.g., `data_A.csv`). If the tarball does not exist, create it.
   - Once successfully archived, delete the original symbolic link in the `staging` directory and replace it with a **hard link** that shares the exact same name as the deleted symlink, but points to the newly updated `.tar.gz` archive.

4. Start your `organizer.py` script in the background.

5. Using shell commands, create the following symbolic links in `/home/user/datasets/staging/`:
   - `neuro_run1.sym` pointing to `/home/user/datasets/raw/data_A.csv`
   - `neuro_run2.sym` pointing to `/home/user/datasets/raw/data_B.csv`
   - `vision_run1.sym` pointing to `/home/user/datasets/raw/data_C.csv`

6. Wait a few seconds for your background Python script to process the symbolic links. 

7. Once the script has processed the links (the symlinks in `staging` will have been replaced by hard links to the archives), stop the background script and write a log file to `/home/user/completion.log` containing the word "DONE".