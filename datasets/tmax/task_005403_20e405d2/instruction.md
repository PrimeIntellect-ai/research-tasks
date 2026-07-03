You are a data engineer tasked with building an ETL pipeline to process surveillance video from an industrial conveyor belt. Recently, a sensor malfunction has been injecting corrupted frames into our video feeds. These corrupted frames disrupt our downstream mathematical modeling and regression tasks, so we need a robust classifier to filter them out.

Your task is divided into three phases:

**Phase 1: Video Extraction (ETL Pipeline)**
1. A video file is provided at `/app/conveyor.mp4`.
2. Write a bash script or command to extract frames from this video at exactly 1 frame per second using `ffmpeg`. Save these frames as JPEG images in `/home/user/extracted_frames/` with the naming convention `frame_0001.jpg`, `frame_0002.jpg`, etc.

**Phase 2: Adversarial Classifier Development**
1. We have provided a set of reference images in `/app/corpus/clean/` (normal frames) and `/app/corpus/evil/` (corrupted frames).
2. The corrupted frames contain a specific mathematical anomaly in their pixel distributions (e.g., extreme shifts in variance, mean channel intensity, or distinct horizontal noise bands) that differentiate them from normal operational variance.
3. Write a Python script `/home/user/detect_corruption.py` that takes a single image file path as a command-line argument.
4. The script must analyze the image and print exactly `CLEAN` to stdout if the image is normal, or `EVIL` if it exhibits the sensor corruption. 
5. You must ensure 100% accuracy on the provided corpora. Avoid hardcoding filenames; the model should use statistical classification or heuristic thresholding based on the image's matrix properties.

**Phase 3: Pipeline Execution & Reporting**
1. Execute your classifier on all frames extracted in Phase 1.
2. Generate a CSV report at `/home/user/frame_report.csv` with the format:
```csv
filename,status
frame_0001.jpg,CLEAN
frame_0002.jpg,EVIL
...
```

Requirements:
- Do not use pre-trained deep learning models (e.g., ResNet). Use basic matrix operations, statistical modeling, or simple classical machine learning (via `numpy`, `scipy`, `scikit-learn`, or `Pillow`/`opencv`).
- Make sure to install any required Python packages using `pip`.