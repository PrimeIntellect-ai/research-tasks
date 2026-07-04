You are assisting a researcher who is organizing datasets from a physics experiment. We have a video recording of a detector's output located at `/app/experiment_data.mp4`. The video consists of 200 frames (grayscale, 64x64 resolution). 

Most frames show only uniform background noise, but in certain frames, a distinct spatial cluster of particles (an anomaly) appears. The researcher previously tried to visualize these frame features using a matplotlib script, but it failed due to a backend misconfiguration, so we are shifting entirely to a C++ based processing pipeline.

Your task is to identify the frames containing the anomaly.

1. Extract the frames from the video. (Hint: You may use `ffmpeg` to extract frames into a simple uncompressed format like PGM, which is trivial to parse manually in C++).
2. Write a C++ program to read the extracted frames and perform feature engineering (e.g., extracting coordinates and intensities of active pixels).
3. Implement statistical modeling / linear algebra in C++ to compute an anomaly score for each frame. For instance, you could compute the spatial covariance matrix of high-intensity pixels and use its determinant or trace, or use Bayesian inference to calculate the likelihood of a localized Gaussian cluster vs. uniform noise. 
4. Higher scores in your output should indicate a higher likelihood of the cluster anomaly being present.
5. Compile and run your C++ program to produce a CSV file at `/home/user/anomaly_scores.csv` with exactly two columns: `frame_id` (integer, 0-indexed corresponding to the frame's position in the video) and `score` (float). Do not include any other columns. A header row `frame_id,score` is required.

An automated verifier will evaluate your scores against the hidden ground truth using the Area Under the Receiver Operating Characteristic Curve (ROC AUC) metric. 

Requirements for Success:
- ROC AUC Score >= 0.90.
- The pipeline must rely on C++ for the mathematical and statistical processing.
- The output file must be exactly at `/home/user/anomaly_scores.csv`.