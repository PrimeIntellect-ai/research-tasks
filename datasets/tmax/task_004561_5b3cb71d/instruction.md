You are a performance engineer tasked with debugging a critical numerical instability in our audio processing pipeline. The Automatic Gain Control (AGC) algorithm is experiencing a convergence failure that eventually leads to application crashes. 

We have isolated the system state right after a crash. 
1. **Database Recovery:** The crash corrupted the profiler's SQLite database located at `/app/profiler.db` (and its WAL file `/app/profiler.db-wal`). Recover the database to read the `crash_logs` table, which contains a crucial hint about the instability.
2. **Audio Analysis:** The exact audio artifact that caused the latest crash has been saved at `/app/incident.wav`. You will need to transcribe the spoken content in this file to find the specific numerical threshold that triggers the convergence failure.
3. **Detector Creation:** Using the insights from the database and the audio transcription, write a Rust CLI application. The application must parse a standard 16-bit PCM WAV file, check for the numerical signature that causes the convergence failure, and reject it.

**Requirements for the Rust Detector:**
- Create your Rust project in `/home/user/detector`.
- Build the project and ensure the final compiled executable is located at `/home/user/detector_bin` (e.g., by copying or symlinking it).
- The executable must accept a single command-line argument: the absolute path to a `.wav` file.
- If the WAV file contains the numerical signature that triggers the convergence failure (the "evil" files), the program must exit with status code `1`.
- If the WAV file does NOT contain the signature (the "clean" files), the program must exit with status code `0`.

Your solution will be tested against a hidden corpus of clean and evil audio files.