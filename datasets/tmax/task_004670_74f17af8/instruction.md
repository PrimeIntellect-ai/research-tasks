As an MLOps engineer, you are auditing our automated experiment artifacts. During a recent run, a matplotlib script produced a visualization video of the experiment telemetry. However, due to a backend misconfiguration, several frames in the video rendered as blank or corrupted plots (e.g., solid color images or mostly blank matrices with very low informational content), while normal frames contain complex data plots.

You need to build a robust detection pipeline.

**Phase 1: Detector Implementation**
Write a Python script at `/home/user/detect_corruption.py`.
- It must take exactly one argument: the absolute path to an image file.
- It must use linear algebra operations (e.g., matrix rank, SVD, or matrix variance via numpy) to determine if the image contains a valid plot or if it is corrupted/blank.
- **Exit Code Requirements**: 
  - If the image is a valid, normal plot (clean), the script must exit with code `0`.
  - If the image is corrupted, blank, or heavily degraded (evil), it must exit with code `1`.
- We have provided a calibration corpus for you to tune your numerical library configurations and thresholds. You will find valid plots in `/app/corpus/clean/` and corrupted plots in `/app/corpus/evil/`. 
- Your script will be tested against a hidden verifier dataset drawn from the same distribution. It must achieve 100% accuracy (reject all evil, accept all clean).

**Phase 2: Video Artefact Analysis**
We have a real experiment video artifact located at `/app/experiment_record.mp4`.
- Use `ffmpeg` (preinstalled) to extract the frames deterministically.
- Analyze every frame using your detection logic.
- Identify the exact 0-indexed frame numbers that are corrupted.
- Output a JSON array of these integer indices to `/home/user/corrupted_frames.json` (e.g., `[12, 45, 88]`).
- Ensure your pipeline is reproducible and deterministic.

**Constraints:**
- Do not use pre-trained deep learning models; rely on structural linear algebra and numerical properties of the image arrays.
- You have full access to a multi-language environment (bash, Python, standard numerical libraries like numpy, cv2, etc.).