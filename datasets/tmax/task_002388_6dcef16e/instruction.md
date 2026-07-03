You are an AI assistant helping a technical writer automate their documentation workflow. The writer drops draft files into a staging directory, and they need a tool to automatically organize these files based on their internal metadata.

Your task is to write a C++ program that watches a directory for new markdown files, reads their metadata, and moves/renames them into an organized folder.

Here are the exact requirements:

1. **Directories**: 
   - Staging directory: `/home/user/staging`
   - Destination directory: `/home/user/organized`
   Create these directories if they do not exist.

2. **The C++ Program**:
   - Write a C++ program at `/home/user/doc_watcher.cpp` and compile it to `/home/user/doc_watcher` (using `g++ -std=c++17`).
   - The program should continuously monitor the `/home/user/staging` directory (a 1-second polling loop is acceptable and robust, or you can use `inotify`).
   - Whenever a `.md` file appears in the staging directory, the program should read its first two lines. The expected format is:
     `Author: <Author Name>`
     `Topic: <Topic Name>`
   - The program must move the file from `/home/user/staging` to `/home/user/organized` and rename it to `<Topic_Name>_<Author_Name>.md`.
   - Any spaces in the Author Name or Topic Name must be replaced with underscores (`_`) in the new filename.
   - If the program detects a file exactly named `HALT` in the staging directory, it should cleanly exit (you don't need to process `HALT` as a markdown file).

3. **Execution & Verification**:
   - Start your compiled `/home/user/doc_watcher` program in the background.
   - Simulate the technical writer's workflow by creating the following three files in `/home/user/staging` (ensure you write the contents correctly, pause briefly if needed to let the watcher process them):
     - `draft1.md` containing:
       `Author: Alice Smith`
       `Topic: API Setup`
       `Content starts here...`
     - `draft2.md` containing:
       `Author: Bob Jones`
       `Topic: Database Config`
       `Content...`
     - `draft3.md` containing:
       `Author: Alice Smith`
       `Topic: User Auth`
       `Content...`
   - After the files have been processed, create the `HALT` file in `/home/user/staging` to stop the background process.
   - Finally, list the contents of `/home/user/organized/` (just the filenames, one per line, sorted alphabetically) and save this output to `/home/user/final_listing.log`.