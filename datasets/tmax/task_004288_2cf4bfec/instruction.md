You are tasked with building a robust incremental backup planning tool in C++ that can gracefully handle complex symbolic link topologies (including infinite loops) and filter files based on a dynamic set of rules.

We have provided a screen recording of the project's backup specification at `/app/backup_spec.mp4`.
1. First, analyze this video. It displays a terminal showing the `BASE_MTIME` (the integer timestamp of the last backup) and a list of `EXCLUDE` patterns (glob-style patterns or exact path prefixes). Extract these values.
2. Write a C++ program at `/home/user/backup_planner.cpp` and compile it to `/home/user/backup_planner`. 
3. Your compiled program must accept a serialized virtual filesystem as a JSON array on standard input (`stdin`). 

**Input JSON Format:**
The input is a JSON array of objects representing nodes in a filesystem.
Example:
```json
[
  {"path": "/src", "type": "directory"},
  {"path": "/src/main.cpp", "type": "file", "mtime": 1680000500},
  {"path": "/src/link_to_src", "type": "symlink", "target": "/src"}
]
```

**Traversal and Logic Requirements:**
- Perform a Depth-First Search (DFS) starting from the root directories (any directory without a parent in the JSON).
- Process children in alphabetical order of their path.
- **Symlink Loops:** You must follow symlinks. If a symlink points to a directory, traverse into it. However, if following a symlink results in visiting a path that is currently in the active DFS path stack (an ancestor in the current traversal line), you MUST detect this as an infinite loop and ignore the symlink.
- **Filtering:** Exclude any resolved paths that match the `EXCLUDE` patterns extracted from the video.
- **Incremental Backup:** Only include files (not directories or symlinks themselves) where `mtime > BASE_MTIME` (the timestamp extracted from the video).

**Output Format:**
Print a CSV to standard output (`stdout`) containing the final resolved logical paths and their mtimes, strictly in the order they were successfully visited by the DFS.
Format: `logical_path,mtime`
Example output (if `/src/main.cpp` matched the criteria):
```csv
/src/main.cpp,1680000500
```

Your program will be rigorously tested against an automated fuzzer that will pipe hundreds of randomized, deeply nested virtual filesystems with adversarial symlink loops to your program to ensure exact behavior equivalence with our internal oracle. Ensure your JSON parsing and DFS loop-detection logic are flawless.