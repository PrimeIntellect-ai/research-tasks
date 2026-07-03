You are assisting a technical writer in indexing a large documentation repository that has been corrupted with recursive symlinks. The documentation system consists of three local services that need to be properly glued together, and a C-based indexer that needs to be made robust.

Your tasks are as follows:

1. **Service Reconfiguration**:
   In `/home/user/services/`, there are three services: an NGINX server serving static files, a Flask API that proxies requests and adds metadata, and a Redis instance used for caching.
   - Start and configure the services so they run correctly. NGINX must listen on port 8080, Flask must listen on port 5000, and Redis on 6379.
   - You must edit `/home/user/services/docker-compose.yml` and `/home/user/services/flask_app/.env` to ensure Flask can connect to Redis and proxy to NGINX correctly.

2. **Indexer Implementation in C**:
   There is a skeleton C program at `/home/user/indexer.c`. The indexer must:
   - Fetch the archive from `http://127.0.0.1:5000/docs.tar`.
   - Use streaming I/O or `mmap` to read the tar file.
   - Verify the archive's integrity (the tar file has a custom 32-byte checksum appended to the very end of the file, representing the XOR of all 512-byte blocks. The C code must calculate and verify this).
   - Parse the tar structure (standard POSIX ustar).
   - Traverse the directories and files within the archive.
   - Detect and skip any infinite symlink loops (e.g., `latest -> ../v1/latest`).
   - Write the canonical absolute paths of all regular files (assuming the archive root is `/`) to `/home/user/valid_files.txt`, one per line.

The final evaluation will test your `/home/user/valid_files.txt`. We will calculate an F1 score matching your list of files against the true, loop-free list of regular files. You must achieve an F1 score >= 0.95.