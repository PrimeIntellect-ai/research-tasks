You are a storage administrator managing disk space for a legacy system that produces massive, highly repetitive log files.

We recently recovered a scanned configuration policy document located at `/app/policy.png`. This image contains crucial archiving parameters for our logging system. 

Your task is to:
1. Extract the archiving policy from the image at `/app/policy.png` (you may use `tesseract` or another OCR tool). The image contains key-value pairs specifying the `LOG_DIR`, `ARCHIVE_DIR`, and `CHUNK_SIZE` (in bytes).
2. Write a Python archiving script at `/home/user/archiver.py` that implements this policy. 
3. The script must:
   - Scan the `LOG_DIR` for `.log` files.
   - Use strict file locking (`fcntl.flock`) on each log file before processing it to ensure no concurrent writes are happening.
   - Split the locked file into binary chunks exactly matching `CHUNK_SIZE` (the final chunk may be smaller).
   - Compress each chunk using `gzip` and save it to `ARCHIVE_DIR` with the naming convention: `[original_filename].chunk[index].gz` (e.g., `app.log.chunk0.gz`, `app.log.chunk1.gz`).
   - Remove the original log file after successful chunking and compression to free up disk space.

Before you begin, create the directories if they don't exist. There is already a large, uncompressed log file waiting in the `LOG_DIR`. Run your script to process this log file. 

The success of your task will be automatically evaluated by calculating the total disk size of `ARCHIVE_DIR`. Since the logs are highly repetitive, your compression implementation must achieve a compressed size of under 2 Megabytes for the test payload.