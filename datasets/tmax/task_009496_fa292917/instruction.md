You are an AI assistant helping a genomics researcher organize a repetitive dataset of synthetic DNA sequences. The researcher needs you to process a large file, chunk it, convert its format, apply a custom compression algorithm, and merge the results into a single archive.

Here are your instructions:

1. **Initial Dataset**: You will find a file at `/home/user/raw_dataset.txt`. It contains 20 lines of repetitive synthetic DNA sequences (only characters A, C, G, T).

2. **File Chunking**: Split the `/home/user/raw_dataset.txt` file into smaller chunks of exactly 5 lines each. Keep the default naming convention of the `split` command (e.g., `xaa`, `xab`, etc.), outputting them in the `/home/user/chunks/` directory. You will need to create this directory.

3. **Format Conversion**: For each chunk file in `/home/user/chunks/`, modify the file in-place (or overwrite it) so that each line is prefixed with its local line number (1 through 5) and a comma. 
   For example, the first line of a chunk becomes `1,AAAAA...` and the fifth line becomes `5,CCCCC...`.

4. **Custom Compression (Bash)**: Write a Bash script at `/home/user/compress.sh` that takes a file path as an argument. The script must read the file and apply a basic Run-Length Encoding (RLE) to the sequence part of the line (after the comma), while keeping the prefix intact. 
   * Example input line: `1,AAAAATTTTTC`
   * Example output line: `1,5A5T1C`
   The script should output the compressed text to standard output. Ensure `/home/user/compress.sh` has executable permissions.

5. **Merging**: Run your `compress.sh` script on each formatted chunk file in alphabetical order. Capture the combined compressed output and save it to a single file at `/home/user/final_dataset.rle`.

Verify your work by ensuring `/home/user/final_dataset.rle` contains exactly 20 lines of properly prefixed and RLE-compressed data.