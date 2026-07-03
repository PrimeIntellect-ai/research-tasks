I am a technical writer trying to organize a massive, messy archive of documentation fragments left behind by an old legacy system. The fragments are scattered across deeply nested directories, some compressed, some plaintext, and contain multi-line metadata mixed with actual content.

I need you to build an automated pipeline using C and Bash to parse, extract, and reassemble these documentation chapters.

Here is the situation:
There is an archive located at `/home/user/legacy_docs.tar.gz`.

**Step 1: Extraction**
Write a shell script at `/home/user/step1_extract.sh` that extracts `/home/user/legacy_docs.tar.gz` into `/home/user/raw_docs/`.

**Step 2: The C Parser**
Write a C program at `/home/user/parser.c` and compile it to `/home/user/parser`. You may use standard libraries and `zlib` (which you may need to install). 
The C program must do the following:
1. Recursively traverse the directory `/home/user/raw_docs/`.
2. Open and read every file it finds. If a file ends in `.gz`, it must stream-process it as a gzip compressed file. If it ends in `.txt`, it reads it as plaintext.
3. Parse the files looking for multi-line documentation records. Records have this exact format:
```
BEGIN_FRAGMENT
Chap: <2-digit Chapter Number>
Part: <2-digit Part Number>
Title: <Chapter Title (only present in Part 01)>
Text:
<Multiple lines of text here>
<More text>
END_FRAGMENT
```
4. For every fragment found, output the exact lines of `<Multiple lines of text here>` to a file in `/home/user/chunks/` named `frag_<Chap>_<Part>.md`. Ensure the `chunks/` directory is created.
5. Whenever it processes a "Part 01" fragment, it must append a mapping line to `/home/user/chapter_index.log` in the format: `Chap_<Chap>:<Title>`. 

**Step 3: Merging and Bulk Renaming**
Write a Bash script at `/home/user/step3_build.sh` that reads the chunks and the index log.
For each chapter in `/home/user/chapter_index.log`, the script must:
1. Identify all fragments for that chapter in `/home/user/chunks/`.
2. Merge them in order of their Part numbers (01, 02, etc.).
3. Save the merged output to `/home/user/final_docs/<Chap>_<Title>.md` (e.g., `01_Introduction.md`). Ensure `final_docs/` is created.

Please execute this pipeline so that the final structured markdown files are populated in `/home/user/final_docs/`. Let me know when you are done.