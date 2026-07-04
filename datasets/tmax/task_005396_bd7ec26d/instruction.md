You are a machine learning engineer building an automated data preparation pipeline for a computer vision model.

We have a raw feed of video footage from a factory floor, but the camera occasionally glitches, producing heavily corrupted frames (e.g., extreme noise, completely solid colors, or severe blur). We need to extract frames from the video, filter out the bad ones using a custom-built model, and store the validated features for downstream training.

Your tasks are:

1. **Video Frame Extraction**:
   Extract frames from the video located at `/app/data/factory_line.mp4` at a rate of 1 frame per second. Store these frames as JPEGs in `/home/user/video_frames/`. Use `ffmpeg`.

2. **Develop a Go-based Anomaly Filter**:
   Write a Go program at `/home/user/pipeline/main.go` and compile it to `/home/user/pipeline/filter`. You may initialize a Go module and use any standard or third-party libraries (e.g., for SQLite or matrix operations).
   The program must operate in two modes:

   **Mode A: Training**
   `./filter --mode train --clean /app/corpus/clean --evil /app/corpus/evil --model /home/user/model.json`
   * Read the images from the provided clean and evil directories.
   * Extract at least two numerical features from each image to represent its quality (e.g., grayscale variance, mean intensity, histogram properties, or PCA-reduced components).
   * Calculate and save boundaries/thresholds (a basic model) that perfectly separate the clean training set from the evil training set into `model.json`.

   **Mode B: Filtering & Storage**
   `./filter --mode filter --input /path/to/input --output /path/to/output --model /home/user/model.json --db /path/to/db.sqlite`
   * Load the `model.json`.
   * Evaluate all JPEG images in the `--input` directory.
   * If an image is classified as "clean", copy it to the `--output` directory. If it is "evil", discard it.
   * For every *clean* image copied, insert its extracted feature values into a SQLite database specified by `--db`. The table should be named `features` with a schema like `(filename TEXT, feature1 REAL, feature2 REAL)`.

3. **Execution**:
   Once your Go program is compiled and ready:
   * Train your model using the corpora provided in `/app/corpus/clean/` and `/app/corpus/evil/`.
   * Run your filtering program on the frames you extracted into `/home/user/video_frames/`, outputting the accepted frames to `/home/user/clean_frames/` and saving the database to `/home/user/features.db`.

Ensure your Go program strictly follows the CLI flags described above. Our automated evaluation system will invoke your compiled `/home/user/pipeline/filter` binary against a hidden adversarial dataset to test its robustness. It must reject 100% of the hidden evil frames and preserve 100% of the hidden clean frames.