You are a support engineer tasked with investigating a diagnostic failure in our video processing pipeline. The pipeline processes diagnostic recordings, but a recent update has caused the backend analyzer to hang (infinite loop) on certain inputs and fail to compile entirely on the latest experimental branch.

Your objectives:

1. **Video Analysis (Diagnostic Artifact):**
   A diagnostic screen recording from the failing system is located at `/app/diagnostics.mp4`.
   Using `ffmpeg` or any other tool, analyze the video frames. The video contains a sequence where the screen flashes pure red (`#FF0000` or close to it due to compression). Count the exact number of completely red frames. 

2. **Git Forensics:**
   Navigate to the local repository at `/home/user/analyzer`.
   The team started working on a fix in a branch named `feature/tz-fix-<N>`, where `<N>` is the number of red frames you found in step 1. Check out this branch.

3. **Compiler and Linker Errors:**
   The code on this branch currently fails to compile due to missing dependencies and a linker error related to a C implementation. Diagnose and fix the build errors so that `go build -o analyzer main.go` succeeds.

4. **Loop Termination and Convergence Fix:**
   The application processes Unix epoch timestamps (provided as a CLI argument). It calculates the epoch timestamp of the *next* midnight in the `America/New_York` timezone. 
   However, the function has a convergence failure: it works by iteratively adding 24-hour durations and strictly checking if `time.Hour() == 0`. Due to Daylight Saving Time (DST) transitions, this loop sometimes skips midnight entirely, resulting in an infinite loop.
   Diagnose the logic, trace the intermediate states, and fix the loop termination bug so it correctly handles DST boundaries without hanging.

5. **Final Output:**
   Ensure your fixed program is compiled to exactly `/home/user/analyzer/analyzer`.
   The binary must take exactly one argument (a Unix epoch integer) and print ONLY the Unix epoch integer of the next midnight in `America/New_York` to stdout.

Do not change the repository path or the final binary path. An automated fuzzing verifier will test your binary against thousands of inputs to ensure bit-exact equivalence with our reference implementation.