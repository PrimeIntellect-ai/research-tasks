You are a web developer building a backend feature for a video analytics platform. We need to process video uploads to detect motion intensity between consecutive frames, which will be served via a web API. To ensure high performance, the core motion analysis is written in C.

Currently, the C codebase and environment are in a broken state. Your goal is to fix the build, patch the code, migrate the database schema, process a sample video, and populate the database with the results.

Here are your instructions:

1. **Video Processing Setup**:
   A sample video is located at `/app/video.mp4`.
   Use `ffmpeg` to extract grayscale frames from this video at 10 frames per second. Save them in `/home/user/frames/` as PGM (Portable Gray Map) files with names formatted as `%04d.pgm` (e.g., `0001.pgm`, `0002.pgm`).

2. **Schema Migration**:
   There is an SQLite database at `/home/user/analytics.db`. It currently has a table `frame_stats` with columns `id INTEGER PRIMARY KEY` and `frame_num INTEGER`.
   You must perform a schema migration to add two new columns to `frame_stats`:
   - `diff_score` (REAL)
   - `timestamp_ms` (INTEGER)

3. **Fix the C Program**:
   The source code is located in `/home/user/src/`. It contains `main.c`, `pgm.c`, `list.c`, and a `Makefile`.
   - **Makefile Repair**: The `Makefile` is currently broken. It fails to compile and link correctly. You will need to fix it. Make sure it links against the math library (`-lm`) and SQLite3 (`-lsqlite3`).
   - **Diff and Patch**: There is a patch file `/home/user/src/list_fix.patch` that partially fixes a bug in the custom doubly-linked list data structure (`list.c`). Apply this patch.
   - **Debugging**: Even after patching, the custom data structure or the diffing logic may have a minor flaw causing segmentation faults or incorrect calculations. Debug and fix the C code so it compiles and runs cleanly.

4. **Run the Analysis**:
   The fixed C executable (named `motion_analyzer`) should take two arguments: the directory containing the frames and the path to the SQLite database.
   ```bash
   ./motion_analyzer /home/user/frames/ /home/user/analytics.db
   ```
   For every consecutive pair of frames (e.g., frame 1 and frame 2, frame 2 and frame 3), the program should calculate the Mean Absolute Difference (MAD) of pixel intensities. The result for the transition ending at frame N should be stored in the database with `frame_num = N`. The `timestamp_ms` should be `(N-1) * 100`.

5. **Verification**:
   An automated test will extract the `diff_score` values from your `analytics.db` and calculate the Mean Squared Error (MSE) against our high-precision reference implementation. Ensure your C program correctly processes all frames and handles the pixel-wise math accurately.