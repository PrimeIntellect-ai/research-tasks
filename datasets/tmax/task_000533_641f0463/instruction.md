You are a storage administrator trying to recover disk space and salvage data from a corrupted storage dump. A legacy backup routine failed and dumped raw data chunks into a single binary file located at `/home/user/data/mixed_backups.bin`. 

Hidden inside this binary file are several gzip-compressed streams. Each gzip stream starts with the standard gzip magic bytes (`0x1F 0x8B`). However, because the disk was failing, some of the data following these magic bytes is corrupted, while other streams are perfectly intact.

Your task is to write and execute a Go program that recovers the intact data. Your Go program must:
1. Scan `/home/user/data/mixed_backups.bin` to find every instance of the gzip magic bytes (`0x1F 0x8B`).
2. Record the exact byte offset of *every* found magic byte sequence to `/home/user/data/gzip_offsets.txt` (write one integer offset per line, in ascending order).
3. For each magic byte sequence found, attempt to read and decompress the gzip stream starting at that offset using standard Go libraries (`compress/gzip`). 
4. If a stream is completely intact (i.e., it decompresses without returning an error until `io.EOF`), append its uncompressed text content to `/home/user/data/recovered_data.txt`. Add a newline (`\n`) after each successfully recovered stream's content. Do not append anything for corrupted streams.

The Go standard library provides everything you need. You may write your Go code to `/home/user/recover.go` and run it. 

Ensure the output files `/home/user/data/gzip_offsets.txt` and `/home/user/data/recovered_data.txt` are formatted correctly as they will be automatically evaluated.