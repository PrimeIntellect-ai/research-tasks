You are an artifact manager tasked with curating binary repositories. Our continuous integration pipeline dumps raw binary files and a multi-line manifest log into an incoming directory. 

You need to write a C program that watches for a specific trigger, parses the multi-line manifest, creates the appropriate nested repository structures, and bulk renames/moves the verified binaries to their final destinations.

Here are the specific requirements:

1. **Directories**: 
   - Incoming directory: `/home/user/incoming`
   - Repository directory: `/home/user/repo`

2. **The Manifest**:
   - Located at `/home/user/incoming/manifest.log`.
   - Contains multi-line records separated by empty lines.
   - Example record format:
     ```
     [Artifact]
     File: raw_101.dat
     Arch: x86_64
     Target: lib/math.so
     Status: verified
     ```
   - Only records with `Status: verified` should be processed. If the status is anything else (e.g., `Status: rejected`), ignore the record.

3. **The C Program (`/home/user/curator.c`)**:
   - Must use Linux `inotify` APIs to watch the `/home/user/incoming` directory.
   - The program should block and wait until a file named `process.trigger` is **deleted** from the `/home/user/incoming/` directory.
   - Once the deletion event is detected, the program must stop watching and process `/home/user/incoming/manifest.log`.
   - For every verified artifact in the log:
     - Construct the final target path: `/home/user/repo/<Arch>/<Target>`
     - Create all necessary intermediate directories (path manipulation/creation).
     - Move and rename the corresponding file from `/home/user/incoming/<File>` to the target path.
   - Finally, the program must write a single line to `/home/user/curator_summary.txt` containing: `Successfully curated: X artifacts` (where X is the number of files moved).

4. **Execution**:
   - Write your code in `/home/user/curator.c`.
   - Compile it to `/home/user/curator` (e.g., `gcc /home/user/curator.c -o /home/user/curator`).
   - Run the compiled binary in the background or let it run (a separate automated process will delete `process.trigger` shortly after your program starts). 
   - Ensure the program exits cleanly after finishing the curation and writing the summary.

Do not assume any maximum length for the manifest log, but no single line will exceed 255 characters.