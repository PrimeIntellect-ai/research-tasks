You are an AI assistant assisting a technical writer with a documentation organization task. 

The writer has a directory `/home/user/docs` containing 50 markdown files named `doc_01.md` through `doc_50.md`.
Each file contains structured metadata and text in the following format (example for file 05):

```text
ID: 05
State: WORK_IN_PROGRESS
Location: /home/user/docs/doc_05.md

Documentation content for item 05...
```

The writer needs to create an automated tool to take a fast snapshot of the documentation and then update the active files for a new release. 

Your task is to write a C program at `/home/user/doc_manager.c` and compile it to an executable named `/home/user/doc_manager`. 
When `/home/user/doc_manager` is executed, it must perform the following operations programmatically:

1. **Snapshot Backup**: Create a directory `/home/user/backup`. For every `.md` file in `/home/user/docs`, create a hard link in `/home/user/backup/` with the exact same filename (e.g., `/home/user/backup/doc_01.md`).
2. **Bulk Rename**: Rename all the files in `/home/user/docs/` to use the prefix `rel_` instead of `doc_` (e.g., `doc_01.md` becomes `rel_01.md`).
3. **Macro Editing**: Modify the contents of the newly renamed `rel_XX.md` files in `/home/user/docs/`:
   - Replace the exact string `State: WORK_IN_PROGRESS` with `State: RELEASED`.
   - Update the `Location:` path to reflect the new filename (e.g., `Location: /home/user/docs/rel_01.md`).

**CRITICAL CONSTRAINT:** The hard-linked files in `/home/user/backup/` MUST retain their original filenames and original content. Modifying the active files in-place (e.g., simply using `fopen(..., "r+")` after renaming) will modify the hard-linked backup data as well, which will ruin the snapshot. Your C program must ensure the edits are safely isolated to the `/home/user/docs/` files so that the backups remain untouched.

Execute your program once it is compiled to complete the task. We will verify the final state of the files.