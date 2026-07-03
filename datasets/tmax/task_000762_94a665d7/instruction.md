You are a technical writer organizing auto-generated system documentation. A background log-rotation script on this server frequently races with the compiler, resulting in corrupted documentation archives. You need to salvage the valid documentation and extract metadata from the compiled binaries to build a master documentation index.

All archives are located in `/home/user/archives/`. There are several `.tar.gz` files in this directory.

Your task is to:
1. Verify the archive integrity of all `.tar.gz` files in `/home/user/archives/`. Ignore any archives that are corrupted, truncated, or fail decompression tests.
2. Extract the contents of the valid archives into a new directory: `/home/user/extracted/`.
3. Inside each valid archive's extracted contents, you will find two files: a Markdown file named `readme.md` and an ELF executable named `app.bin`.
4. Use the `readelf` utility to parse the ELF headers of each `app.bin` and extract its exact "Entry point address" (e.g., `0x401000`).
5. Combine the extracted information into a single text file located at `/home/user/docs_summary.txt` using standard stream redirection. 
6. The final `/home/user/docs_summary.txt` file must contain exactly one line per valid archive in the following format:
   `<archive_filename> | <first_line_of_readme.md> | <entry_point_address>`
   
   *Example line:*
   `arch_alpha.tar.gz | # Core Engine | 0x401050`

7. Sort the lines in `/home/user/docs_summary.txt` alphabetically by the archive filename.

Make sure your summary matches the format precisely, including the spaces around the pipe `|` characters. You may use shell built-ins, coreutils, and standard CLI tools to accomplish this.