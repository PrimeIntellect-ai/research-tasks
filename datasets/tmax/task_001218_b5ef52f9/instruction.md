You are an AI assistant helping a backup administrator recover and archive data after a storage corruption event. 

During the recovery process, several files were salvaged into the `/home/user/recovery/inbox/` directory, but their original file extensions were lost or scrambled (they might end in `.dat`, `.tmp`, `.bin`, etc.). 

Your task is to:
1. Identify the true file type of every file in `/home/user/recovery/inbox/` based on its binary header / MIME type.
2. Move and rename these files into the `/home/user/recovery/organized/` directory, assigning them the correct extension based on their MIME type:
   - `image/png` should have a `.png` extension.
   - `application/pdf` should have a `.pdf` extension.
   - `text/plain` should have a `.txt` extension.
   - `application/gzip` should have a `.gz` extension.
   *Note: Preserve the original base name of the file. For example, `file1.dat` should become `file1.png` if it is a PNG image.*
3. Create an incremental backup archive named `/home/user/backup_incr.tar` that contains *only* the files in the `/home/user/recovery/organized/` directory that have a modification timestamp **newer** than the reference file `/home/user/recovery/last_backup.stamp`. 
4. The tar archive should contain just the files themselves (e.g., `file2.pdf`), without any leading directories like `home/user/...` or `organized/`.

Ensure all operations are completed via the terminal. Use standard bash commands and coreutils (like `file`, `find`, `tar`, `cp`, `mv`).