You are a machine learning engineer preparing training data and building a baseline model to track the progress of a mechanical process recorded in a video. We have a calibration video located at `/app/calibration_video.mp4`. 

Your goal is to build an end-to-end ETL and modeling pipeline orchestrated entirely via Bash scripts. You need to extract features from the video, build a dataset, and train a lightweight regression model to predict the frame index (time) solely from the linear algebra properties of the frame.

Here are the specific requirements:

1. **ETL Extraction (`extract.sh`)**:
   - Write a bash script that uses `ffmpeg` to extract all frames from `/app/calibration_video.mp4` as grayscale JPEG images into a directory `data/frames/`.
   - Scale the extracted frames to exactly 128x128 pixels.

2. **Feature Engineering & Linear Algebra (`compute_features.sh` and auxiliary scripts)**:
   - For each extracted frame, compute its top 5 Singular Values (SVs) treating the 128x128 grayscale image as a matrix.
   - You may write a brief Python script to compute the SVD, but the orchestration and processing loop must be handled in Bash (e.g., using `find`, `xargs`, or bash `for` loops).
   - Compile these features into a CSV file named `data/dataset.csv` with the header: `frame_idx,sv1,sv2,sv3,sv4,sv5`. The `frame_idx` is the integer index of the frame (starting at 1).

3. **Modeling & Tuning (`train.sh`)**:
   - Write a script that trains a Ridge Regression model to predict `frame_idx` from the 5 singular values.
   - Use 5-fold cross-validation to tune the hyperparameter `alpha` (test at least `[0.1, 1.0, 10.0]`).
   - Use a bootstrap method (e.g., 100 resamples) to compute the 95% confidence interval of your cross-validation Mean Absolute Error (MAE), and log this to `data/metrics.log`.
   - Save the final tuned model weights (e.g., using `pickle` or `joblib`) to `model.pkl`.

4. **Inference Interface (`inference.sh`)**:
   - Write a bash script `inference.sh` that takes a single argument: the path to a 128x128 grayscale JPEG image.
   - The script should output *only* the predicted frame index (as a floating-point number or integer) to standard output.

5. **Pipeline Master (`pipeline.sh`)**:
   - A single executable script that sequentially runs the extraction, feature computation, and training steps, building the entire environment from scratch.

Your final deliverable will be evaluated using a hidden test set of frames generated from a similar mechanical process. The verifier will call your `./inference.sh` on these hidden frames. Your model's Mean Absolute Error (MAE) must be below 20.0 frames.