A researcher in our lab has a massive archive of legacy dataset files. Unfortunately, many files in the dataset have been corrupted or contain malformed text encodings that cause our proprietary indexing tool to crash (segfault) or hang indefinitely.

We have provided a stripped, compiled version of this legacy indexer at `/app/legacy_indexer`. 

Your tasks are as follows:

1. **Extract the Corpora**: In `/home/user/raw_data/`, there is a multi-part archive named `corpora.tar.gz.parta`, `corpora.tar.gz.partb`, etc. Recombine and extract them. Inside the extracted archive, you will find two directories: `clean/` (files that the indexer safely processes) and `evil/` (files that cause the indexer to crash or hang).

2. **Reverse-Engineer the Format**: Analyze the `/app/legacy_indexer` binary and the provided `clean` and `evil` files to deduce the file format requirements. The indexer expects a specific binary header and strict character encoding rules for the payload. Corrupted files violate one or more of these undocumented rules.

3. **Write a Sanitizer in C**: Write a C program at `/home/user/filter.c` and compile it to `/home/user/filter`. 
    * The program must accept a single file path as a command-line argument: `./filter <path_to_file>`.
    * It must read the file (handling binary and text data appropriately).
    * It must validate the file against the rules you deduced.
    * It must exit with status `0` if the file is perfectly valid ("clean").
    * It must exit with status `1` if the file violates any format or encoding rules ("evil").

The automated grading suite will invoke your compiled `/home/user/filter` against a hidden validation set of clean and evil files. To pass, your filter must correctly preserve 100% of the clean corpus (exit 0) and reject 100% of the evil corpus (exit 1) without crashing.