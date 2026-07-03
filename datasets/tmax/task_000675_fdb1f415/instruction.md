You are assisting a researcher who is organizing a large archive of datasets located at `/home/user/dataset`. To avoid duplicating data, the researcher used symbolic links extensively. However, they suspect that some of these symlinks accidentally create circular references (infinite loops) where a directory contains a symlink pointing to one of its parent directories, or to another directory that links back to it.

Your task is to write a C program that identifies these problematic symlinks. 

Requirements:
1. Create a C program at `/home/user/find_loops.c`.
2. The program must recursively traverse the directory `/home/user/dataset`.
3. It must detect any symbolic link that, if followed, would result in an infinite traversal loop (e.g., a symlink pointing to an ancestor directory, or a mutually recursive symlink loop between directories). 
4. The program must output the absolute paths of all such "loop-causing" symlinks into a strictly formatted JSON array file at `/home/user/loops.json`.
5. The JSON file should contain exactly one array of strings. Example format:
```json
[
  "/home/user/dataset/dirA/link_back",
  "/home/user/dataset/dirB/dirC/another_link"
]
```
6. The order of the paths in the JSON array does not matter, but the paths must be absolute.
7. Compile and run your C program to produce the `/home/user/loops.json` file.

Do not use external libraries other than standard POSIX C libraries (e.g., `<dirent.h>`, `<sys/stat.h>`, `<unistd.h>`).