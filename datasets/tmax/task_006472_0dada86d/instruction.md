You are an AI assistant helping a technical writer organize a legacy documentation dump. 

The writer has received a nested archive located at `/home/user/docs_archive.tar.gz`. 
Here is what you need to do:

1. **Extract the nested archives:** 
   The `docs_archive.tar.gz` file contains several `.zip` files. Extract all of them. Inside these zip files, you will find several encoded document files with names following the pattern `DOC_<id>_OLD.txt.rle` (e.g., `DOC_001_OLD.txt.rle`).

2. **Bulk Renaming:**
   Rename all extracted `.txt.rle` files to lowercase and change "old" to "new". For example, `DOC_001_OLD.txt.rle` must be renamed to `doc_001_new.txt.rle`. Keep them in the same directory they were extracted to, or move them to a single directory like `/home/user/docs/`.

3. **Custom Decompression and Decoding (C Programming):**
   These `.rle` files use a custom Run-Length Encoding (RLE) combined with a simple character shift encoding. 
   Write a C program at `/home/user/decoder.c` that compiles to `/home/user/decoder`.
   The program must read an input file and write to an output file (e.g., `./decoder input.rle output.txt`).
   - The binary format of the `.rle` file consists of pairs of bytes: `[count][char]`.
   - `count` (unsigned 8-bit integer) is the number of times the character repeats.
   - `char` (8-bit) is the encoded character. To decode it to standard ASCII, you must subtract 5 from its integer value (e.g., if the byte is 'f' (102), the decoded character is 'a' (97)).
   - For each pair, write the decoded character `count` times to the output file.

4. **Process and Combine:**
   Use your compiled C program to decode all the `doc_<id>_new.txt.rle` files into standard text files named `doc_<id>_new.txt`.
   Finally, concatenate all the decoded text files in strictly increasing numerical order of their `<id>` into a single final file at `/home/user/final_docs.txt`.