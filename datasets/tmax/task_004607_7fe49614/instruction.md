You are a Data Engineer building an ETL pipeline for a smart surveillance system. Your goal is to process video footage, extract features, and build a probabilistic filter that detects anomalous ("evil") frames while allowing normal ("clean") frames to pass through.

You must accomplish the following steps:

1. **Environment Setup**: Install any necessary system packages (e.g., `ffmpeg`, `imagemagick`) and Python packages (e.g., `scikit-learn`, `numpy`, `opencv-python`) required for video processing and Bayesian inference.

2. **Video Processing**: 
   A surveillance video is located at `/app/data/video.mp4`.
   Extract frames from this video at exactly 1 frame per second (fps) into the directory `/home/user/frames/`. Name the extracted frames sequentially, e.g., `frame_001.jpg`, `frame_002.jpg`, etc.

3. **Classifier Development**:
   We have provided a training/validation corpus of images under `/app/corpus/`.
   - `/app/corpus/clean/` contains images of normal conditions.
   - `/app/corpus/evil/` contains images with anomalies.
   
   You must train a Bayesian classification model (e.g., Gaussian Naive Bayes) to distinguish between clean and evil images based on their visual features (e.g., color histograms or brightness metrics). 
   Your modeling process must include cross-validation to tune hyperparameters (such as variance smoothing).
   
4. **Adversarial Filter Script**:
   Write a Bash script at `/home/user/filter.sh` that takes exactly one argument (the path to an image file).
   - The script must exit with status code `0` if the image is classified as "clean".
   - The script must exit with status code `1` if the image is classified as "evil".
   This script will be tested against a hidden holdout corpus. It must achieve 100% accuracy on the provided `/app/corpus/` directories to pass.

5. **Inference & Benchmarking**:
   Run your `filter.sh` against all the frames you extracted into `/home/user/frames/`.
   - Write the filenames of all frames detected as anomalous (evil) to `/home/user/anomalies.txt` (one filename per line, e.g., `frame_015.jpg`).
   - Benchmark the inference performance of your pipeline over the extracted frames. Calculate the inference speed in frames per second (FPS) and write this single numerical value to `/home/user/fps.txt`.

Ensure your Bash script efficiently wraps your Python/inference logic.