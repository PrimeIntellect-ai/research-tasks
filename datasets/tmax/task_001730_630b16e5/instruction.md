I'm a technical writer, and I've received a massive dump of documentation from various engineering teams. The upstream system that generated this export is buggy: it nested archives inside other archives, and worse, it lost the file extensions for many of the inner archive files (naming them `.dat` or `.bin`). 

I need you to help me extract all the Markdown documentation from this mess.

Here is the setup:
You have a starting archive located at `/home/user/docs_archive.tar`. 
Inside it, there are Markdown files (`.md`), as well as other archive files (which could be Zip files or Gzipped Tarballs). Some of these inner archives have correct extensions, but others end in `.dat` or `.bin`. You cannot rely on the file extensions to know if a file is an archive. 

Your task:
1. Write a Python script at `/home/user/parse_docs.py` that recursively traverses and extracts the archives.
2. The script must identify archives by inspecting their binary file signatures (magic numbers/headers), specifically looking for ZIP files (`PK\x03\x04`) and GZIP files (`\x1f\x8b`).
3. For every standard file found in the extraction tree, if it has an `.md` extension, read its contents.
4. Your script must output the concatenated contents of all discovered `.md` files to standard output (stdout). 
5. To ensure a predictable output, sort the discovered `.md` files alphabetically by their base filename (e.g., `a.md` before `b.md`, ignoring directory paths) before printing their contents.
6. For each `.md` file, print `### FILE: <basename>` on one line, followed by the exact file contents on the next lines, followed by a blank line.
7. Finally, run your script and use standard shell redirection to pipe its output into `/home/user/compiled_docs.md`.

Do not hardcode the names of the files in your script, as the structure is dynamic. Use standard Python libraries (`zipfile`, `tarfile`, `os`, `io`, etc.).