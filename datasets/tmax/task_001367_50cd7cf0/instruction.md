You are helping a researcher organize and extract custom `.zres` dataset archives. These archives use a proprietary binary compression format developed by the lab.

Unfortunately, the lab's C++ extraction library has a critical security flaw: it is vulnerable to a path traversal attack (similar to "Zip Slip"). Maliciously crafted archives can overwrite files outside the intended extraction directory. Furthermore, the library currently fails to compile due to a broken Makefile.

You must complete the following multi-stage workflow:

1. **Fix the Vendored Package:**
   Navigate to `/app/zres_lib-1.2.0`. Fix the `Makefile` so it successfully compiles `libzres.a`. Then, modify the extraction logic in `zres.cpp` to strictly reject any archive that attempts path traversal (e.g., file paths starting with `/` or containing `../`). If an invalid path is detected, the extraction function must throw a `std::runtime_error("Path traversal detected")` and abort immediately.

2. **Implement the Dataset Organizer:**
   Write a C++ program at `/home/user/organizer.cpp` that links against `/app/zres_lib-1.2.0/libzres.a`.
   Your program must be invokable via the command line:
   `./organizer <archive_path.zres> <output_directory>`
   
   The program must perform the following:
   - Call the library's extraction function to extract the archive into `<output_directory>`.
   - If the library throws the path traversal exception, catch it, print "MALICIOUS ARCHIVE REJECTED" to standard output, and exit with status code 1.
   - If extraction is successful, look for a file named `metadata.log` inside `<output_directory>`.
   - Read `metadata.log`, which contains multi-line records in the following format:
     ```
     OriginalName: data_1.bin
     NewName: sensor_alpha_01.bin
     ---
     OriginalName: data_2.bin
     NewName: sensor_beta_02.bin
     ---
     ```
   - Perform bulk file renaming within `<output_directory>` according to these records. Delete `metadata.log` after renaming is complete. Exit with status code 0.

Compile your program into an executable named `organizer` in `/home/user/`.

Ensure your code is robust. The system will test your `organizer` executable against two sets of archives: a "clean" corpus that must be correctly extracted and renamed, and an "evil" corpus containing path traversal exploits that must be strictly rejected.