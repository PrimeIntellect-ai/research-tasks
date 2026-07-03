I need your help managing a live dataset stream for my research. A background process is currently generating high-speed sensor data and appending it to a file at `/home/user/live_sensor.log`. 

The data is writing so quickly that I need a Python script to continuously "rotate", chunk, compress, and organize it without interrupting the writer process. 

Please write and execute a Python script located at `/home/user/archiver.py` that does the following:
1. Continuously reads `/home/user/live_sensor.log` as it is being written (similar to `tail -f`). Use streaming I/O so you don't load the whole file into memory.
2. Splits the incoming data into chunks of exactly 10,000 lines.
3. As soon as a chunk reaches 10,000 lines, save it temporarily, and then compress it into a gzip-compressed tar archive (`.tar.gz`). Store these archives in `/home/user/dataset_archive/` with the naming convention `chunk_1.tar.gz`, `chunk_2.tar.gz`, etc.
4. Manage a symbolic link at `/home/user/dataset_archive/latest.tar.gz`. Every time a new chunk archive is successfully created, update this symlink to point to the newly created archive.
5. The dataset writer will stop exactly after 50,000 lines. Once your script has successfully created all 5 chunk archives (`chunk_1.tar.gz` through `chunk_5.tar.gz`), bundle these 5 `.tar.gz` files into a single, uncompressed tarball located at `/home/user/final_merged.tar`.
6. Finally, write the exact string "SUCCESS" to a file at `/home/user/status.txt` and exit.

Constraints:
- Do not modify or stop the writer process.
- Each `chunk_N.tar.gz` must contain exactly one file named `chunk_N.txt` containing the 10,000 lines for that chunk.
- The `latest.tar.gz` symlink must be a relative or absolute link that correctly resolves to the latest archive.
- Ensure your Python script is robust and correctly handles the end of the 50,000 lines. You can run your script to process the data and fulfill the requirements.