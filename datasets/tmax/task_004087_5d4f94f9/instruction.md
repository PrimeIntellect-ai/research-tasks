You are an MLOps engineer tasked with building an automated tracking pipeline for physical experiment artifacts. A camera has recorded an experiment, and the video is available at `/app/experiment_record.mp4`.

The experiment consists of three distinct physical phases, but the exact boundaries are unknown. You need to build a pipeline that extracts features from the video and uses probabilistic modeling to automatically cluster the frames into these three phases.

Please create a Bash orchestrator script at `/home/user/run_pipeline.sh` that does the following when executed:
1. Installs any necessary Python dependencies for computer vision and machine learning.
2. Uses `ffmpeg` (which is already installed) to extract the frames from `/app/experiment_record.mp4` at exactly 1 frame per second (1 fps) into a temporary directory.
3. Executes a Python script (which you must also write, e.g., `/home/user/extract_and_model.py`) that performs the data science tasks:
   - Loads all extracted frames in grayscale and flattens them into 1D vectors. Ensure the frames are sorted chronologically by their extraction index.
   - Performs Dimensionality Reduction on the flattened frames using Principal Component Analysis (PCA), reducing the feature space to exactly 5 principal components.
   - Fits a Bayesian Gaussian Mixture Model (from `scikit-learn`'s `BayesianGaussianMixture`) to the 5-dimensional data. Configure it to search for exactly `n_components=3` with a `full` covariance type, and a `random_state=42`.
   - Assigns each frame to one of the 3 cluster components based on the maximum posterior probability.
4. Saves the results to a CSV file at `/home/user/artifact_phases.csv` with exactly two columns: `frame_index` (integer, 0-indexed chronologically) and `phase_cluster` (integer 0, 1, or 2 representing the assigned Bayesian GMM cluster).

Requirements:
- Your Bash script must have execute permissions (`chmod +x`).
- Do not hardcode the number of frames, as the video length may vary.
- Your final output `/home/user/artifact_phases.csv` must include a header: `frame_index,phase_cluster`.
- The task is complete when I can successfully run `./run_pipeline.sh` and see the generated `artifact_phases.csv`.