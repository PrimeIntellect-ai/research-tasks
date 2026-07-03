Hello! I'm trying to organize a highly chaotic project repository, and I need your help building a reliable pipeline to sanitize the configuration files and recover some lost metadata.

We have a custom build configuration format (JSON files containing embedded dependency expressions) that has been polluted with malicious directory traversal attacks by a compromised script. We also have an old visual log of the project's file creation events that we need to extract data from.

Here is what I need you to do:

**Part 1: Video Metadata Recovery**
There is a video file located at `/app/file_events.mp4`. This video is a visual log of file events. Every frame represents a moment in time. When a new valid file was added to the project, the top-left 10x10 pixels of the video frame flashed pure green (RGB: 0, 255, 0). 
1. Use `ffmpeg` and any other bash-available tools to extract the frames and analyze them.
2. Count the exact number of frames where the top-left 10x10 pixel block is predominantly pure green. 
3. Write this integer to the first line of `/home/user/project_summary.log`.

**Part 2: C++ Configuration Sanitizer**
The project configuration files use JSON. Inside these JSON files, there is a key called `"depends_on"`, which contains a string representing a custom expression. The expression syntax supports:
- `file("path")` : denotes a dependency on a specific file.
- `concat(expr1, expr2)` : concatenates two strings.
- `parent(expr)` : evaluates to the parent directory of the path.

For example: `concat(parent(file("src/main.cpp")), "/utils.hpp")` evaluates to `"src/utils.hpp"`.

You must write a C++ program, source code at `/home/user/sanitizer.cpp`, that takes a single file path as a command-line argument.
1. The program must parse the JSON file and extract the `"depends_on"` expression.
2. It must parse and evaluate the expression to its final string path.
3. **Security Check**: If the evaluated final path attempts to traverse outside the current working directory (e.g., contains `../` in its resolved, normalized form, or resolves to an absolute path like `/etc/passwd`), the file is considered malicious.
4. If the file is malicious, the program must exit with status code `1` and print "REJECTED".
5. If the file is safe, the program must exit with status code `0` and print "ACCEPTED".
6. Compile this program to an executable located at `/home/user/sanitizer`.

To help you develop this, I have provided a corpus of configuration files:
- `/app/corpora/clean/`: Contains valid, safe configuration files. Your sanitizer MUST exit with `0` for all of these.
- `/app/corpora/evil/`: Contains malicious configuration files that use clever expression combinations to traverse directories. Your sanitizer MUST exit with `1` for all of these.

**Part 3: Final Output**
Once your C++ program is compiled and works perfectly against the test corpora, append the path of your compiled executable to the second line of `/home/user/project_summary.log`.

Good luck!