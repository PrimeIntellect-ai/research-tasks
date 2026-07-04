I am a researcher trying to organize a large dataset, but I've run into a problem. My colleague sent me a compressed dataset archive located at `/home/user/dataset.tar.gz`. 

Inside this tarball, there are several `.zip` files representing different experiments (e.g., `experiment_1.zip`, `experiment_2.zip`). Inside those `.zip` files are gzip-compressed text files (`*.txt.gz`) containing JSON lines data. 

However, there's a trap in the archive: a buggy backup script created an infinite symlink loop (`loop_dir` points back to `.`) inside the tarball. Standard recursive extraction commands (like `tar -xzf`) get stuck or fail.

I need you to write a Go program at `/home/user/process_dataset.go` that can bypass this symlink trap. Your Go program must:
1. Open and read the `/home/user/dataset.tar.gz` archive.
2. Ignore any symlinks or directories.
3. Find all `.zip` files inside the tarball.
4. Extract and process the contents of these `.zip` files in memory or via temporary files.
5. Inside the `.zip` files, find all `*.txt.gz` files.
6. Decompress the `*.txt.gz` streams.
7. Parse the uncompressed JSON lines. Each line is a JSON object.
8. Filter for objects where the key `"status"` has the exact string value `"valid"`.
9. Write the matching JSON lines to `/home/user/valid_records.jsonl` (one valid JSON object per line).

You must use Go to solve this. Ensure you handle the nested archives and compressed streams correctly. 

Once your program is written, execute it to produce the final `/home/user/valid_records.jsonl` file. Do not change the JSON formatting of the filtered lines, just write them exactly as they appeared uncompressed.