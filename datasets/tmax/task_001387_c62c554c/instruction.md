As an artifact manager curating our legacy binary repositories, we are migrating our binary blobs to a new storage backend. We need to implement a packing utility for our custom legacy format (Format V3). 

Unfortunately, the text specification for Format V3 was lost during a wiki migration, but I managed to recover a screenshot of the documentation. The screenshot is located at `/app/spec.png`. You will need to extract the rules from this image (you can use tools like `tesseract`, which is preinstalled).

Your task is to write a Python 3 script at `/home/user/archiver.py` that perfectly implements this packing process.
The script must:
1. Read raw binary data from standard input (`stdin`).
2. Pack the data into the Format V3 archive format exactly as specified in the recovered image (handling the specific character encoding for the header, the exact chunking rules, the binary length prefixes, and the custom byte-level transformation).
3. Write the resulting binary archive to standard output (`stdout`).

We have a recovered binary executable of the original packer at `/app/oracle_archiver`. You can use this to test your implementation. Your Python script must be bit-for-bit identical in its output to `/app/oracle_archiver` for any given input. 

Please ensure `/home/user/archiver.py` exists, is executable, and strictly reads from `stdin` and writes to `stdout` without printing any extraneous debug information to `stdout`.