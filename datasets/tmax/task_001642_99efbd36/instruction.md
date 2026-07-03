You are tasked with organizing a messy project directory left behind by a former developer. The developer left a video screencast of the project, but more importantly, embedded the archive packaging configuration inside the video's metadata. 

Here is your objective:

1. **Extract the Configuration:**
   The file `/app/project_screencast.mp4` contains a base64-encoded configuration file hidden in its `comment` metadata tag. Extract this metadata (e.g., using `ffprobe` and `jq`), decode it from base64, and save it to `/home/user/packaging.conf`. 
   The configuration maps file types to their target archive paths, in the format `TYPE:ARCHIVE_PATH`.

2. **Identify and Organize Files:**
   The directory `/home/user/messy_project/` contains dozens of files. However, their file extensions have been randomized or removed. You must recursively traverse this directory and identify files based on their actual content formats:
   *   **ELF**: Executable and Linkable Format files.
   *   **WAL**: SQLite Write-Ahead Log files.
   *   **GCODE**: 3D printer manufacturing files (text files containing the string `M109` and at least one `G1` movement command).
   
   Ignore any file that does not match one of these three formats.

3. **Create the Archives:**
   Using the mapping from your extracted `/home/user/packaging.conf`, create the specified archives. 
   *   Put all identified ELF files into the archive specified for `ELF`.
   *   Put all identified WAL files into the archive specified for `WAL`.
   *   Put all identified GCODE files into the archive specified for `GCODE`.
   
   *Note: Ensure the files within the archives do not contain their absolute paths (store them at the root of the archive).*

4. **Serve the Archives:**
   Start an HTTP server listening on `127.0.0.1:8080` that serves the directory containing the newly created archives. You may use any standard tool available in the environment to serve the directory (e.g., `python3 -m http.server`, `ruby -run -e httpd`, or a custom bash/socat loop).

Leave the HTTP server running in the background so it can be verified.