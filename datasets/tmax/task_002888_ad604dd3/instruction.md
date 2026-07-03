I am a technical writer, and our legacy documentation build system recently broke. It followed a recursive symlink loop and dumped all of our documentation into a single massive, concatenated text file, which it then compressed. I need your help to parse this file, fix the encoding, split it back into its original files, and repackage it.

You must accomplish this by writing a C program.

Here are the specific details:
1. There is a compressed file located at `/home/user/legacy_manual.gz`. 
2. The uncompressed content is plain text encoded in `ISO-8859-1` (not UTF-8).
3. The concatenated file contains multiple distinct documentation pages. Each page is separated by a specific delimiter line: `==== DOC_START: <filename> ====` (where `<filename>` is the target file name, like `intro.txt` or `api_v1.txt`). There is no text before the first delimiter.
4. You need to write a C program named `/home/user/doc_parser.c` that:
   - Uses `zlib` (`gzopen`, `gzgets`, etc.) to read the compressed stream directly (do not uncompress it to disk first).
   - Uses `iconv` to convert the text from `ISO-8859-1` to `UTF-8` on the fly.
   - Parses the delimiters and splits the content.
   - Writes the UTF-8 converted text of each section to its corresponding `<filename>` inside the directory `/home/user/recovered_docs/`. (You must create this directory).
5. Compile your C program (you may need to install `zlib1g-dev` and link `-lz`) and run it to perform the extraction.
6. Once the C program has successfully populated `/home/user/recovered_docs/` with the split UTF-8 files, use shell commands to create a tarball of this directory at `/home/user/clean_docs.tar.gz`. The tarball should contain the files directly or within a `recovered_docs` folder.
7. Finally, generate a log file at `/home/user/recovery.log` containing the exact filenames (one per line, sorted alphabetically) that were recovered and extracted.

Please write the C program, compile it, run it, create the final archive, and write the log file.