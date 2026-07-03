You are assisting a technical writer who needs an automated way to process large documentation drafts into smaller, manageable chunks.

Your task is to write a C++ program that watches a specific directory for new text files, splits them into smaller Markdown chunks, and generates an index file containing the normalized absolute paths to these chunks.

Here are the specific requirements:

1. **Directories**: 
   - Watch Directory: `/home/user/doc_watch`
   - Output Directory: `/home/user/doc_processed`
   (Assume these directories already exist or create them in your C++ code).

2. **The C++ Program (`/home/user/doc_daemon.cpp`)**:
   - Write a C++ program that runs continuously. It should check the `/home/user/doc_watch` directory every 1 second for new files with the `.txt` extension.
   - When a new file (e.g., `draft.txt`) is detected, the program must:
     a. Read the file.
     b. Create a new directory in the output path named after the file (e.g., `/home/user/doc_processed/draft/`).
     c. Split the contents of the text file into multiple Markdown files (`part_1.md`, `part_2.md`, etc.) inside that new directory. Each chunk must contain exactly **3 lines** of text from the original file, except for the last chunk which may contain fewer if the total line count is not divisible by 3.
     d. Create an `index.md` file in the new directory (e.g., `/home/user/doc_processed/draft/index.md`). This index file must contain a list of the **absolute, normalized paths** to each generated chunk file, one path per line, in ascending order (part_1.md, part_2.md, etc.).
     e. Delete the original file from `/home/user/doc_watch` so it is not processed again.

3. **Execution**:
   - Compile your program to an executable named `/home/user/doc_daemon`.
   - Run the executable in the background (e.g., `./doc_daemon &`) so it is actively watching the directory.
   - Leave the background process running when you complete your turn.

Ensure your code handles path manipulation cleanly and includes all necessary standard library headers (like `<filesystem>`, `<fstream>`, `<thread>`, `<chrono>`, etc.).