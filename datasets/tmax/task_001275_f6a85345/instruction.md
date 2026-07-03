You are an artifact manager curating a binary repository. We receive continuous streams of custom binary archives that need to be parsed, decompressed, and curated. 

Your tasks are:

1. **Understand the Format**: There is an image file at `/app/magic_spec.png` that contains the specification for our proprietary binary artifact header format. Extract the text from this image to understand how to parse the binary streams. 

2. **Develop the Extractor**: Write a C++ program at `/home/user/extractor.cpp` and compile it to `/home/user/extractor`. 
   - It must read a continuous binary stream from `stdin` and write to `stdout`.
   - It must strictly implement the parsing, decompression, and error-recovery rules found in the image specification.
   - Your compiled binary must be **bit-exact equivalent** in its standard I/O behavior to our closed-source reference implementation located at `/app/oracle_extractor`. It will be tested against millions of bytes of randomized and corrupted input streams.

3. **Curate the Repository**:
   - We have a staging area at `/app/incoming/` containing deeply nested subdirectories.
   - Use metadata-based search to find all files in `/app/incoming/` that have a size strictly greater than 1024 bytes AND have the setuid bit (`u+s`) set.
   - Using standard stream redirection and piping, concatenate the contents of all these matching files and pipe them through your newly compiled `/home/user/extractor`.
   - Save the stdout of the extractor to `/home/user/final_manifest.txt`.

4. **Link Management**:
   - Each line in `/home/user/final_manifest.txt` will contain an absolute file path.
   - Determine which of those files has the most recent modification timestamp.
   - Create a symbolic link at `/home/user/latest_artifact` pointing to that specific file.
   - For all other files listed in the manifest, create hard links to them inside a new directory `/home/user/curated_archive/` (keeping their original basenames).

Make sure your C++ code is robust, links against necessary compression libraries, and properly handles standard streams.