I am a technical writer trying to organize a messy set of documentation files I received from the engineering team. 

I have an archive located at `/home/user/incoming_docs.tar.gz`. Inside this archive, there are several `.zip` files, which in turn contain various markdown (`.md`) and text files representing different pieces of documentation.

I need you to do the following:
1. Extract the main archive and all nested `.zip` archives.
2. Find all `.md` files that contain the exact line `Status: PUBLISHED`.
3. Concatenate the full contents of only these published markdown files into a single text file at `/home/user/release_manual.md`. When concatenating, please process the files in alphabetical order based on their filename (e.g., `a.md` before `b.md`).
4. Finally, package this single generated file into a new gzip-compressed tar archive located at `/home/user/release.tar.gz`.

Please complete this task using whichever scripts or shell commands you prefer.