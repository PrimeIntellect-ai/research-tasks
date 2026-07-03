As a technical writer, I need your help organizing inline API documentation from our C codebase into a single consolidated file, while ensuring concurrent access safety. 

We have a custom tool written in C that appends text to a file, but it currently lacks file locking. Other background processes (like automated linters) might write to the documentation file at the same time, so we must ensure our writes are safely locked.

Here is what you need to do:

1. **Fix the Append Tool:** 
   Look at `/home/user/tools/safe_append.c`. This program reads from standard input and appends to a file provided as the first argument. It is missing the file locking mechanism. Modify the code to apply an exclusive lock (`LOCK_EX`) using `flock()` on the file descriptor before writing, and unlock it (`LOCK_UN`) after writing.
   Compile the fixed program to `/home/user/tools/safe_append`.

2. **Parse and Extract Documentation:**
   We have several C source files in `/home/user/src/`. You need to extract all multi-line documentation blocks that begin exactly with `/* API` on a line by itself, and end exactly with `*/` on a line by itself.
   
3. **Format and Append:**
   Read the configuration file at `/home/user/docs.conf`. It contains a single line: `PREFIX=<some_string>`.
   For every line inside the extracted API blocks (excluding the `/* API` and `*/` lines), prepend the prefix from the config file, followed by a space. 
   Pipe this formatted text into your compiled `/home/user/tools/safe_append` tool to safely append it to `/home/user/api_docs.md`.

Process the files in alphabetical order (e.g., `module_a.c` then `module_b.c`).

**Example:**
If `docs.conf` has `PREFIX=DOC` and `module_a.c` contains:
```c
/* API
Function: init_system
Returns: int
*/
```
The text appended to `/home/user/api_docs.md` should be:
```
DOC Function: init_system
DOC Returns: int
```