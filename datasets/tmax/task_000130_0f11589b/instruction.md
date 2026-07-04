I need your help building a secure dataset ingestion pipeline for my research lab. We have multiple researchers uploading datasets, but we've had issues with malformed archives and accidental path traversal overwrites.

We have a multi-service setup running in `/home/user/pipeline/`:
1. A Python upload server (FastAPI) running on port 8000 that receives `.tar` files and saves them to `/home/user/pipeline/incoming/`. It pushes the path of the uploaded file to a Redis list named `dataset_queue`.
2. A Redis instance running on port 6379.

Your task is to write a Rust daemon (`/home/user/pipeline/processor/src/main.rs`) that:
1. Connects to Redis (port 6379) and blocks on the `dataset_queue` list.
2. For each tar file path popped from the queue, uses memory-mapped I/O to quickly scan the tar header.
3. Implements an adversarial filter:
   - It must REJECT any tar archive containing files with absolute paths or paths containing `../` (path traversal).
   - It must REJECT any tar archive containing symbolic links that point outside the extraction directory.
   - It must ACCEPT valid tar archives.
4. If accepted, safely extracts the tarball to `/home/user/pipeline/extracted/<dataset_name>/` (where `<dataset_name>` is the tar filename without the `.tar` extension).
5. For each extracted dataset, generates a manifest file at `/home/user/pipeline/manifests/<dataset_name>.manifest` containing the SHA-256 checksums of all files in the dataset, formatted as `<checksum>  <relative_filepath>\n`.
6. To save disk space, all identical files across different valid datasets must be hard-linked together in `/home/user/pipeline/extracted/`. You must use file locking (e.g., `flock` on a global lock file `/home/user/pipeline/hardlink.lock`) during the hard-linking phase to prevent race conditions.

You must write the Rust application in `/home/user/pipeline/processor/` (a Cargo project is already initialized there but empty) and write a bash script `/home/user/pipeline/start_all.sh` that starts the Python server, Redis, and your Rust daemon. 

The test will invoke `/home/user/pipeline/start_all.sh`, wait for services to be up, and then submit a batch of clean and malicious tarballs to port 8000. It will check that malicious tarballs are completely ignored (not extracted, no manifest) and clean tarballs are properly extracted, deduplicated via hardlinks, and correctly manifested.