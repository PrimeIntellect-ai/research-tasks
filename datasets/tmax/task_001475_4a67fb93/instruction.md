You are a data engineer building the first stage of an ETL pipeline that processes visual sensor data from a factory floor. 

We have a video feed recording from a sensor located at `/app/factory_feed.mp4`. We need to extract an environmental metric from this video, store the raw extracted data efficiently, and compute a statistical summary using bootstrap methods.

Please perform the following steps:
1. Ensure any necessary Python libraries (e.g., `opencv-python`, `pandas`, `pyarrow`, `scipy`, `numpy`) are installed.
2. Write a Python script to process the video `/app/factory_feed.mp4`. For every single frame in the video, convert the frame to grayscale and calculate the average pixel intensity (a float value representing the mean across all pixels in that frame).
3. Save this extracted time-series data to a Parquet file at `/app/processed_frames.parquet`. The file should contain a single column named `intensity` representing the chronological sequence of frame intensities.
4. Perform a bootstrap analysis to estimate the 95% confidence interval of the mean frame intensity across the entire video. 
   - Use exactly **10,000** bootstrap resamples.
   - Use the percentile method to determine the lower (2.5%) and upper (97.5%) bounds.
   - Set the random seed for your bootstrap sampling to `42` (e.g., `np.random.seed(42)`) to ensure reproducibility.
5. Save your final statistical summary to `/app/metrics.json`. The JSON file must have exactly three keys:
   - `"mean"`: The sample mean of the frame intensities.
   - `"ci_lower"`: The lower bound of the 95% bootstrap confidence interval.
   - `"ci_upper"`: The upper bound of the 95% bootstrap confidence interval.

Round the values in the JSON to 4 decimal places.