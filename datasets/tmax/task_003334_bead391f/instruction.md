You are an MLOps engineer managing an artifact tracking pipeline for a reinforcement learning project. The agent's rollouts are saved as video files, but due to a rendering bug, some frames are corrupted and render as completely dark/black screens. These corrupted frames are ruining our downstream image embedding and retrieval systems. 

You need to build a Bash-based sanitization pipeline that detects and rejects these corrupted frames, and then apply it to process a new rollout.

Step 1: Build the Filter
Write a Bash script at `/home/user/filter.sh` that takes a single image file path as its first argument.
- The script must analyze the image (you may install and use `ImageMagick`).
- If the image is corrupted (mean brightness/luminance is extremely low, e.g., less than 5%), the script must exit with code `1` (Reject).
- If the image is normal/clean, the script must exit with code `0` (Accept).
- We have provided a test corpus for you to calibrate your script: `/app/corpora/clean/` contains valid frames, and `/app/corpora/evil/` contains corrupted dark frames. Our automated verifier will strictly test your script against a hidden holdout set of similar images.

Step 2: Process the Video Artifact
A new experimental rollout is located at `/app/rollout.mp4`.
1. Use `ffmpeg` to extract frames from this video at exactly 1 frame per second (1 fps). Save the extracted frames to `/home/user/frames/` using the naming format `frame_0001.png`, `frame_0002.png`, etc.
2. Iterate through all extracted frames and run your `/home/user/filter.sh` on each.
3. Delete any frames from `/home/user/frames/` that your filter rejects.
4. For all surviving (clean) frames, compute their SHA-256 hash (using `sha256sum`) to serve as the exact retrieval key for the embedding database.

Step 3: Generate the Final Report
Create a reproducibility log at `/home/user/valid_rollout.csv`.
The file must contain a header `filename,sha256` and list the surviving frames sorted alphabetically by filename.
Example format:
```
filename,sha256
frame_0001.png,a1b2c3d4...
frame_0003.png,e5f6g7h8...
```

Ensure your `filter.sh` is robust and your pipeline is completely automated.