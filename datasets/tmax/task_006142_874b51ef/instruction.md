You are tasked with helping a configuration management team process a massive backlog of server configuration changes. 

We have a large, compressed log file located at `/home/user/server_configs.log.gz`. Due to strict disk space limitations on this jump server, you are **not** allowed to decompress this file to disk. 

The log file contains a history of configuration changes. Each line follows this pipe-delimited format:
`TIMESTAMP | SERVER_ID | ACTION | CONFIG_KEY | VALUE`

Your objective is to write and execute a Python script that processes this compressed log as a stream. You must extract all lines where the `ACTION` is `UPDATE` and the `CONFIG_KEY` is `db_timeout`.

Because downstream systems can only handle small batches, you must split these extracted, matching lines into chunked, gzipped files inside a new directory called `/home/user/db_timeout_updates/`. 

Requirements:
1. Stream the input file (`/home/user/server_configs.log.gz`) without extracting it.
2. Filter for lines matching `ACTION == UPDATE` and `CONFIG_KEY == db_timeout`.
3. Output the matching lines into gzipped chunk files in `/home/user/db_timeout_updates/`.
4. The output files must be named `update_chunk_0.log.gz`, `update_chunk_1.log.gz`, `update_chunk_2.log.gz`, etc.
5. Each output chunk must contain exactly 500 lines, except for the final chunk which should contain whatever matching lines remain.
6. The output lines must retain their exact original formatting from the input log.

Create and run the Python script to complete this task.