You are a storage administrator managing a Linux server that is critically low on disk space. A legacy application has been dumping logs and data files into `/home/user/storage_pool/`. Over time, these files have been archived inconsistently, resulting in deeply nested archives (tarballs inside zips, multi-part zips, etc.), and massive data duplication.

Your manager has left a screenshot of the new storage policy at `/app/policy.png`. You must:
1. Extract the text from the image to discover the target maximum disk space allowed and the master password used for any encrypted legacy archives in the storage pool.
2. Write a Bash script at `/home/user/optimize_storage.sh` that processes `/home/user/storage_pool/`.
3. The script must recursively traverse the directory and extract all archives (handling `.zip`, `.tar.gz`, and nested combinations thereof). Use the password found in the image for any encrypted `.zip` files.
4. After fully extracting all data to bare files, identify and remove all duplicate files across the entire dataset (files with identical content, regardless of their filenames). Keep only one copy of each unique file.
5. Combine and highly compress all the remaining unique files into a single archive located at `/home/user/optimized_pool.tar.xz`.
6. Remove all original and intermediate files in `/home/user/storage_pool/`, leaving only the `optimized_pool.tar.xz` file on disk.

To succeed, you will likely need to install OCR tools like `tesseract-ocr`, handle recursive unarchiving in Bash, script a deduplication routine based on file hashes, and utilize aggressive `xz` compression settings. 

Your final archive's size will be scored against the threshold metric defined in the policy image.