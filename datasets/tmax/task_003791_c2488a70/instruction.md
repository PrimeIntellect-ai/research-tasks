You are an AI assistant helping a technical writer organize and update a batch of legacy documentation.

We have an archive of legacy documentation located at `/home/user/legacy_docs.tar.gz` and a configuration file located at `/home/user/build.conf`. 

Your task is to automate the extraction, transformation, and repackaging of these documents according to the following steps:

1. **Extraction:** Extract the contents of `/home/user/legacy_docs.tar.gz` into a new directory `/home/user/extracted_docs/`.
2. **Configuration Parsing & Text Replacement:** 
   Read `/home/user/build.conf`. It contains lines specifying text replacements in the format `REPLACE:OldString:NewString`. 
   Apply all these replacements to every file inside `/home/user/extracted_docs/` using `sed`, `awk`, or a similar tool.
3. **Custom Space Compression (C++):**
   The configuration file also contains a line like `COMPRESS_EXT:.txt`, which defines a file extension. 
   You must write a C++ program at `/home/user/compressor.cpp` and compile it to `/home/user/compressor`. 
   This program must read a text file, find any sequence of **2 or more consecutive space characters (' ')**, and replace that sequence with `&N&`, where `N` is the exact number of spaces. (For example, "Hello   World" becomes "Hello&3&World"). Single spaces should be left completely unchanged.
4. **Apply Compression:**
   Run your compiled `/home/user/compressor` on all files in `/home/user/extracted_docs/` that match the extension specified by `COMPRESS_EXT` in the configuration file. The compression should modify the files in-place (or overwrite the original files with the compressed versions, keeping the same filenames).
5. **Repackaging:**
   Create a new gzip-compressed tarball at `/home/user/final_docs.tar.gz` containing the contents of `/home/user/extracted_docs/`. The root of the tarball should contain the files directly (or the `extracted_docs` directory, either is fine as long as the files are inside).

Make sure your C++ code handles standard input/output or file paths properly, and ensure all transformations are applied exactly as specified.