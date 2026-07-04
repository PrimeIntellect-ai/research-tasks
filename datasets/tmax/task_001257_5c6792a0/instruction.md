I am a technical writer managing a large, messy repository of documentation. I need a robust Go program to process, merge, and chunk my Markdown files according to a configuration file, ensuring that the final output is written atomically so my continuous deployment pipeline never reads partially written files.

Please write a Go program at `/home/user/doc_builder.go` that does the following:

1. **Read Configuration**: Parse `/home/user/config.json`. It will have this structure:
   ```json
   {
     "source_dir": "/home/user/docs",
     "output_dir": "/home/user/dist",
     "max_lines_per_chunk": 50,
     "merge_groups": {
       "getting_started.md": ["intro.md", "setup/install.md"]
     }
   }
   ```
2. **Traverse and Accumulate**: Recursively traverse all `.md` files in `source_dir`. 
   - If a file's relative path (e.g., `intro.md` or `setup/install.md`) is listed in a merge group, concatenate its contents into the specified target file (`getting_started.md` in this case). Files must be merged in the exact order they appear in the JSON array.
   - If a file is NOT part of any merge group, it should remain separate, keeping its base filename (ignoring its subdirectories). For example, `advanced/networking.md` becomes `networking.md`.
3. **Chunking**: For every resulting document (merged or standalone), check its total line count.
   - If it exceeds `max_lines_per_chunk`, split it into multiple files. Name them `[basename]_part1.md`, `[basename]_part2.md`, etc. (1-indexed). The first chunks should have exactly `max_lines_per_chunk` lines, and the final chunk will have the remainder.
   - If it does not exceed the limit, keep the original name (e.g., `getting_started.md`).
4. **Atomic Writes**: To prevent race conditions in my CD pipeline, your program MUST write the output chunks using temporary files. Create a temporary file, write the chunk's content, close it, and then use `os.Rename` to atomically move it into the `output_dir`.
5. **Execution**: Create the program, then compile and run it so that it processes `/home/user/docs` and populates `/home/user/dist`. Ensure `output_dir` is created if it doesn't exist.

Ensure the final `/home/user/dist` directory contains the accurately merged and chunked files before finishing.