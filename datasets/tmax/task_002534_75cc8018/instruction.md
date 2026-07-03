You are assisting a technical writer in recovering and organizing an archived set of documentation. 

A previous internal tool merged, compressed (via a simple XOR cipher), and concatenated multiple Markdown files into a single binary blob located at `/home/user/docs_blob.bin`. 

You are provided with a configuration file at `/home/user/split.conf` which dictates how this blob should be split. Each line in the config file follows the format:
`filename:offset:length`

There is a skeleton C program at `/home/user/extractor.c`. Your task is to complete this C program so that it:
1. Parses `/home/user/split.conf` to get the target filename, offset, and length.
2. Reads the appropriate chunk from `/home/user/docs_blob.bin`.
3. "Decompresses" the chunk by XORing every byte with the key `0x42`.
4. Saves the decoded text to the `/home/user/output/` directory (you must create this directory first). 
5. Important: The C program must use `flock()` (from `<sys/file.h>`) to acquire an exclusive lock (`LOCK_EX`) on each output file before writing to it, as this tool will later be used in a multi-threaded writer environment.

Once you have completed `extractor.c`, compile it using standard `gcc` to `/home/user/extractor` and run it so that the original markdown files are properly extracted to `/home/user/output/`.