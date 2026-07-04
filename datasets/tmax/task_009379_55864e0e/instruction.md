You are a backup administrator tasked with archiving a continuous stream of log data while maintaining strict data integrity. A legacy application generates logs continuously, and we need a tool to safely chunk this data, verify its integrity, and archive it on the fly.

Your task is to write a C program that reads log data from standard input (`stdin`), chunks it into manageable files, creates a manifest with checksums, and then archives the entire batch.

Specifically, write a C program at `/home/user/archiver.c` and compile it to `/home/user/archiver` with the following requirements:
1. It must read text lines continuously from `stdin`.
2. It must write the input lines into chunked files located in the directory `/home/user/archive_dir/`. (Create this directory in your program or via shell before running).
3. The chunk files must be named `chunk_1.txt`, `chunk_2.txt`, `chunk_3.txt`, etc.
4. Each chunk file must contain exactly 50 lines of logs, except the last one, which will contain whatever remaining lines exist before EOF.
5. As soon as a chunk file is closed, your program must compute its MD5 checksum and append a line to `/home/user/archive_dir/manifest.txt` in the exact format: `<md5sum>  chunk_<N>.txt` (two spaces between the sum and the filename). You may use external system commands like `md5sum` within your C code.
6. When EOF is reached on `stdin` and the final chunk is closed and manifested, the C program must create a compressed archive of the directory at `/home/user/final_backup.tar.gz` containing all chunks and the manifest. The archive should be created such that extracting it yields the files directly or within an `archive_dir` folder. 

Once your C program is compiled, a pre-existing script located at `/home/user/generator.sh` will produce the mock log stream. Execute the process by piping the generator to your compiled archiver:
`/home/user/generator.sh | /home/user/archiver`

Verify your implementation ensures `/home/user/final_backup.tar.gz` is created successfully and contains the correct chunk files and manifest.