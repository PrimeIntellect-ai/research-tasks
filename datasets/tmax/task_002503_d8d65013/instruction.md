Our continuous integration (CI) pipeline for a legacy C++ application is failing entirely. The build system processes a large corpus of text-based asset files, but it is crashing mid-build. We lost the standard output logs due to a misconfigured CI runner, but we do have a screen recording of the terminal session during the crash, a core dump, and the corrupted SQLite database used for build caching.

Your objective is to diagnose the root cause of the crash, identify the malformed payload, and write a filter script to sanitize the asset corpus.

Here are the resources available to you:
1. **CI Screen Recording:** `/app/ci_screen.mp4` - A video of the terminal during the build. The build tool crashed, and a linker or compiler error flashed on screen just before the runner terminated. 
2. **Build Cache Database:** `/app/build_state/cache.db` - The SQLite database tracking processed assets. It was corrupted during the crash, but its WAL (Write-Ahead Log) file is present in the same directory.
3. **Core Dump:** `/app/build_state/core.dump` - The memory dump from the crashed build process.

Perform the following tasks:

**Step 1: Diagnose Environment & State**
* Extract the frames from `/app/ci_screen.mp4` (ffmpeg is installed). Inspect the final frames to identify the exact missing shared library that the linker complained about.
* Recover the SQLite database from the WAL file. Query the `processed_files` table to find the name of the last successfully processed asset before the crash.

**Step 2: Memory Dump Analysis**
* Analyze `/app/build_state/core.dump` to find the malicious string payload that caused the parser to crash. You know it is a highly distinctive macro expansion trigger that starts with `[[[MACRO` and ends with `]]]`.

**Step 3: Create the Corpus Filter**
* Write a script at `/home/user/filter_assets.sh`.
* The script must take exactly two arguments: an input directory and an output directory (`/home/user/filter_assets.sh <input_dir> <output_dir>`).
* It must evaluate all `.asset` files in the input directory.
* If a file contains the malicious macro payload you discovered in the core dump, it must NOT be copied.
* If a file does not contain the payload, it MUST be copied to the output directory with its original filename.
* The script must be executable.

**Step 4: Reporting**
* Create a file at `/home/user/debug_report.txt` containing exactly two lines:
  * Line 1: The name of the missing shared library found in the video.
  * Line 2: The filename of the last successfully processed asset found in the recovered database.