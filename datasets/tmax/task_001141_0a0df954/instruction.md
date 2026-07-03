I am a researcher organizing visual datasets from our laboratory experiments. We record videos of our experiments, but our camera hardware is failing and frequently drops frames, resulting in completely black or heavily glitched (pure static noise) frames. I need to automate the extraction and cleaning of these datasets.

You need to perform the following steps:

1. **Environment & Setup**: You can install any standard Python machine learning or computer vision libraries you need (e.g., `scikit-learn`, `opencv-python`, `xgboost`, `Pillow`).
2. **Model Training**: I have provided a training dataset of previously extracted frames. 
   - `/app/corpus/clean/` contains valid, usable experimental frames.
   - `/app/corpus/evil/` contains corrupted, dark, or noisy frames we must reject.
   Extract features (e.g., mean pixel intensity, variance, edge density) and train a robust classifier to distinguish between the two. Perform cross-validation and hyperparameter tuning to ensure the model generalizes perfectly to basic camera failures. Save your trained model to disk.
3. **Filtering Script**: Create a script named `/home/user/filter_dataset.py` with the following CLI signature:
   `python3 /home/user/filter_dataset.py <input_dir> <output_dir>`
   This script must load your trained model, evaluate every image (`.jpg` or `.png`) in `<input_dir>`, and copy *only* the images predicted to be "clean" into `<output_dir>`.
4. **Video Processing**: I have a new raw recording at `/app/experiment_video.mp4`. 
   - Use `ffmpeg` to extract frames from this video at exactly 1 frame per second into `/home/user/raw_frames/`. Name them `frame_001.jpg`, `frame_002.jpg`, etc.
   - Run your `filter_dataset.py` script to filter `/home/user/raw_frames/` and output the valid frames to `/home/user/clean_frames/`.
5. **Reporting**: Generate a `/home/user/report.json` file with the following exact keys:
   - `"total_raw_frames"`: integer count of frames extracted from the video.
   - `"total_clean_frames"`: integer count of frames that survived the filter.
   - `"cv_accuracy"`: float representing your model's cross-validation accuracy on the training corpus (e.g., 0.99).

Please complete all steps so that I can automatically verify your `filter_dataset.py` script against a holdout dataset of clean and evil frames.