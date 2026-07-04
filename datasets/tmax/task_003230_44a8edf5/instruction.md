You are an artifact manager curating binary repositories. You have inherited a repository of proprietary legacy artifacts with the extension `.artb` (Artifact Bundles). The only tool available to extract these bundles is a stripped, undocumented ELF executable located at `/app/decode_artb`. 

Your goal is to write a Python 3 script at `/home/user/decode_artb.py` that perfectly replicates the behavior of `/app/decode_artb`. 

The tool reads an `.artb` file from `stdin` and writes the uncompressed binary data to `stdout`. You must figure out the binary format and decompression scheme by analyzing the binary or treating it as a black-box oracle. 

Some hints about the `.artb` format:
- It involves extracting a binary format and headers.
- It uses file chunking.
- It uses a custom compression scheme (a form of Run-Length Encoding).

Your Python script must be bit-exact equivalent to the oracle binary for any valid `.artb` input. It should read from `stdin` and write the decompressed data to `stdout`. Make sure your script handles standard I/O properly in Python (e.g., using `sys.stdin.buffer` and `sys.stdout.buffer`).

Do not hardcode specific file paths in your script; it must strictly operate on standard input and output.