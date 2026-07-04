You have inherited an unfamiliar and poorly written Python codebase located in `/home/user/videophysics/`. The previous developer wrote a pipeline to extract optical signal entropy from a high-speed physics experiment video. 

The pipeline script is intended to process the video located at `/app/experiment.mp4`, but it currently fails to complete successfully. You are facing two main issues:
1. **Intermittent Corruption/Missing Data:** The pipeline extracts frames and processes them concurrently to speed up execution. However, the output logs and the resulting CSV often have garbled or interleaved lines, and sometimes frame records are completely missing or dropped. You'll need to dig into the concurrency model and logs to find and fix the race condition.
2. **Deterministic Crashes (Numerical Instability):** Even when running sequentially or with a single thread, the program frequently crashes with a `ValueError: math domain error` or a `ZeroDivisionError` on specific frames (e.g., when the video flashes black or white during the experiment). You must diagnose the mathematical instability in the entropy calculation module and implement a robust mathematical fix (e.g., epsilon addition or valid domain clipping) without fundamentally changing the analytical formula.

Your objective:
1. Debug and patch the Python scripts in `/home/user/videophysics/` to be thread-safe and mathematically stable.
2. Run your patched pipeline on the video `/app/experiment.mp4`.
3. Output the final successfully processed data to `/home/user/final_output.csv`.

The final CSV must have a header `frame_index,entropy` and contain a row for every single frame in the video, sorted by `frame_index` in ascending order. The `entropy` column should be a floating-point number.

Do not use heavy external ML libraries like PyTorch or TensorFlow; the standard library and lightweight libraries (like `Pillow` or standard CLI tools like `ffmpeg`) are sufficient and pre-installed.