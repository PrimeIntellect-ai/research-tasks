I am a technical writer trying to recover some old documentation from a legacy custom archive format. I have a large binary archive file located at `/home/user/doc_archive.bin`.

The archive is essentially a concatenated stream of files, where each file is prefixed by a binary header. I need you to write a C program that uses `mmap` (Memory-Mapped I/O) to parse this archive, extract all files that have a `.md` extension, and save them into the directory `/home/user/docs_extracted/`. 

Here is the exact format of the archive:
It consists of back-to-back entries. Each entry has:
1. `filename`: A 16-byte character array, null-padded if the name is shorter than 16 characters.
2. `size`: A 32-bit unsigned integer (little-endian) representing the size of the file data.
3. `data`: The actual file data of `size` bytes.

Your tasks:
1. Create the directory `/home/user/docs_extracted/`.
2. Write a C program (save it as `/home/user/extractor.c`) that memory-maps `/home/user/doc_archive.bin` and iterates through the chunks.
3. For every chunk where the filename ends with `.md`, write its `data` to a new file in `/home/user/docs_extracted/` with the corresponding filename.
4. Compile and run your C program.
5. Once the markdown files are extracted, use standard Linux utilities to create a compressed tarball of the extracted `.md` files at `/home/user/markdown_archive.tar.gz`. Do not include the directory structure in the tarball (the `.md` files should be at the root of the archive).

Please proceed and leave the final `markdown_archive.tar.gz` in `/home/user/`.