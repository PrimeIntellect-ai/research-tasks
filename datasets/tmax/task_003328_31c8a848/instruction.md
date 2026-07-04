You are an AI assistant helping a technical writer migrate a massive collection of legacy documentation into a unified, optimized custom archive.

Your environment contains the following:
1. `/home/user/docs_data.sqfs`: A SquashFS filesystem image containing legacy documentation files.
2. `/app/ldoc_decoder`: A stripped Linux binary from the legacy system. It takes two arguments: an input `.ldoc` file and an output file path.
3. `/home/user/build_config.json`: A configuration file specifying which documents to include in the final archive and their intended directory structure.

Here is your workflow:

**Phase 1: Extraction and Decoding**
1. Mount the `/home/user/docs_data.sqfs` image to `/home/user/mnt`.
2. Inside the mounted directory, you will find several `.ldoc` files. These are proprietary legacy documents. Use the `/app/ldoc_decoder` binary to extract them into raw `.html` files.

**Phase 2: Format Conversion**
1. Convert the decoded `.html` files into standard Markdown (`.md`). You may use standard Python libraries (like `beautifulsoup4` or `markdown`) to strip HTML tags and convert basic elements (h1, p, a, etc.) into Markdown equivalents.

**Phase 3: Configuration and Filtering**
1. Read `/home/user/build_config.json`. It contains a list of allowed filenames and their target logical paths in the final archive. Ignore any extracted files not present in this configuration.

**Phase 4: Custom Archiving (Python)**
Write a Python script `/home/user/pack_docs.py` that takes the filtered `.md` files and packs them into a highly optimized custom archive format at `/home/user/final.docz`. 

The `.docz` file format MUST strictly follow this structure:
- **Bytes 0-3**: The ASCII magic string `DOCZ`.
- **Bytes 4-7**: A 32-bit unsigned integer (little-endian) representing the byte size of the JSON index (`S`).
- **Bytes 8 to 8+S-1**: A UTF-8 encoded JSON string containing a dictionary. Keys are the logical file paths (from the JSON config), and values are arrays of two integers `[offset, length]` representing the start offset and uncompressed length of that file's data within the concatenated payload block.
- **Bytes 8+S onwards**: The Zlib-compressed (level 9) payload. The payload is simply the raw byte concatenation of all the included Markdown files in the exact order they appear in the JSON index. (Compress the ENTIRE concatenated block at once, not file-by-file, to maximize compression).

**Verification**
Your task is complete when `/home/user/final.docz` is created successfully. An automated verifier will parse your archive, check its integrity against the config, and measure its final file size. To pass, your implementation must achieve a tight compression ratio resulting in a file size below a strict numerical threshold.