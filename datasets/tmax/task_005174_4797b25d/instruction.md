You are an ETL data engineer. We have a traffic camera video located at `/app/traffic.mp4` (25 frames per second, 320x240 resolution). Your goal is to build a reproducible pipeline in C and Bash that processes this video, extracts tabular motion metrics, and applies a Bayesian probabilistic model to estimate traffic congestion.

Please create a pipeline script at `/home/user/run_pipeline.sh` that does the following:

1. **Dependency Management**: Installs any needed tools (e.g., `ffmpeg`, `gcc`).
2. **C Program Compilation**: Compiles a C program (which you must write) at `/home/user/etl_processor.c`. 
3. **Data Extraction & Aggregation**: Uses `ffmpeg` to decode `/app/traffic.mp4` into a raw grayscale (luma only) video stream, which is piped directly into your C program. 
4. **Motion Metric Processing**: Your C program must read the stream frame-by-frame and compute the "motion score" for each frame. The motion score is defined as the mean absolute difference in pixel intensities between the current frame and the previous frame. The first frame has a motion score of 0.
5. **Windowing**: Group the frames into 1-second tumbling windows (25 frames per window). Window 0 is frames 0-24, Window 1 is frames 25-49, etc. For each window, compute the average motion score (the mean of the 25 frame motion scores).
6. **Bayesian Inference**: For each window, calculate the posterior probability that the road is "congested" (State $C=1$) versus "clear" (State $C=0$), given the window's average motion score $M$.
   - Assume a prior probability $P(C=1) = 0.3$.
   - The likelihood of $M$ given $C=0$ follows a Gaussian distribution with $\mu_0 = 2.0$ and $\sigma_0 = 1.5$.
   - The likelihood of $M$ given $C=1$ follows a Gaussian distribution with $\mu_1 = 15.0$ and $\sigma_1 = 5.0$.
   - Compute the posterior $P(C=1 | M)$ using Bayes' theorem.
7. **Reporting**: The C program must output a CSV file to `/home/user/traffic_report.csv` with a header `window_id,avg_motion,p_congested`. The `p_congested` column should be formatted to 4 decimal places.

Your bash script should execute automatically and leave the final CSV in place. We will test your script by checking if the resulting `traffic_report.csv` contains accurate probabilities compared to a reference standard.