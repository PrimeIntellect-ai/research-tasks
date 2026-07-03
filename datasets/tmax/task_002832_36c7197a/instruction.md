Hello, I am a researcher working with a large, messy dataset that I've inherited from a previous lab member. I need your help organizing, verifying, and repackaging this data using a Bash shell. 

Currently, there is a multi-part archive located at `/home/user/raw_dataset/`. It consists of several split files named `dataset.tar.gz.partaa`, `dataset.tar.gz.partab`, etc. 

Please perform the following data curation pipeline:

**Phase 1: Assembly and Base Extraction**
1. Reassemble the split archive parts into a single valid `tar.gz` archive.
2. Extract the contents of this reassembled archive into a new directory: `/home/user/processing/`.

**Phase 2: Nested Archive Integrity and Extraction**
Inside `/home/user/processing/`, you will find several nested archives (some `.zip`, some `.tar.gz`).
1. Verify the integrity of every nested archive. 
2. If an archive is **corrupted** or invalid, DO NOT extract it. Instead, append its exact filename (just the basename, e.g., `bad_data.zip`) to `/home/user/corrupted_archives.log`.
3. If an archive is **valid**, extract its contents into `/home/user/extracted/<archive_name_without_extension>/`. (For example, `subject1.tar.gz` should be extracted to `/home/user/extracted/subject1/`).

**Phase 3: Link Management and Deduplication**
The extracted dataset is known to contain broken symbolic links and duplicated files, which waste space.
1. Recursively search through `/home/user/extracted/` and **delete** any broken symbolic links.
2. Find all regular files within `/home/user/extracted/` that have exactly identical content. Consolidate these duplicates by replacing them with **hard links** to a single instance of the file, thereby saving disk space. (All identical files must share the same inode).

**Phase 4: Repackaging**
1. Once the extraction, cleanup, and deduplication are complete, create a new archive of the cleaned dataset at `/home/user/clean_dataset.tar.bz2`.
2. This new archive must contain the entire contents of the `/home/user/extracted/` directory.
3. Ensure that your archiving command **preserves the hard links** you created, so the final archive doesn't bloat in size.

Please write and execute the necessary Bash commands or scripts to accomplish this. Rely only on standard Linux coreutils, `tar`, `gzip`, `bzip2`, and `unzip`.