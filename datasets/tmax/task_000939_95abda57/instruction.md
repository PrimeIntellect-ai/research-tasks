Hello, IT Support. We have an urgent ticket escalated to us from the data processing team. 

Our Rust-based video metadata analyzer is failing in production. It processes incoming motion tracking payloads associated with a specific video file. However, we are facing several issues:
1. **Environment Misconfiguration:** The project fails to build because it can't find the necessary C libraries. It seems a build script or environment configuration is broken.
2. **Serialization and Core Dumps:** The application frequently panics and generates core dumps when processing certain payloads. This seems to be tied to improper deserialization and out-of-bounds array access related to frame indices.
3. **Convergence Failure:** The motion stabilization algorithm (`refine_motion`) occasionally gets stuck in an infinite loop instead of converging, causing the application to hang.

The source code is located in `/home/user/video_analyzer`.
A sample video associated with these payloads is located at `/app/video_fixture.mp4`. 

**Your Objective:**
1. Fix the environment or build scripts so the Rust project compiles successfully.
2. Debug and fix `src/main.rs` to resolve the core dumps, serialization crashes, and the infinite loop (convergence failure).
3. Build a standalone filter binary to validate incoming payloads. The executable MUST be located at `/home/user/video_analyzer/target/release/payload_filter`.

**Requirements for `payload_filter`:**
- It must accept exactly one CLI argument: the path to a JSON payload file.
- It must dynamically determine the total number of frames in `/app/video_fixture.mp4` (you may use `ffprobe` or `ffmpeg` as system commands to inspect the video).
- It must attempt to deserialize the JSON and process it using the fixed `refine_motion` algorithm.
- If the file is a valid payload, all frame indices are within the actual bounds of the video, and the algorithm converges successfully within 100 iterations, it must exit with code `0`.
- If the JSON is malformed, specifies frame indices greater than or equal to the total frames in the video, or the algorithm fails to converge within 100 iterations, it must exit with code `1` (or any non-zero exit code).
- The binary MUST NOT crash, panic, core dump, or hang infinitely on any input.

Please leave the compiled binary at `/home/user/video_analyzer/target/release/payload_filter` when you are done.