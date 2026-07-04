You are an ML Engineer preparing training data. We need to analyze an experiment video and set up an API to serve the results. 

There is an existing script at `/home/user/analyze.py` that processes the video located at `/app/experiment_feed.mp4`. 

The script is supposed to:
1. Extract frames from the video at 1 frame per second.
2. Calculate the mean grayscale pixel intensity for each extracted frame.
3. Use a bootstrap method (1000 resamples) to compute the 95% confidence interval of the mean intensity across all sampled frames.
4. Log the experiment results (mean, lower_bound, upper_bound) to `/home/user/tracking.json`.
5. Plot a histogram of the bootstrap distribution and save it as `bootstrap_dist.png`.

However, the script currently produces a blank/empty plot due to a matplotlib misconfiguration (it saves the figure before plotting, or fails due to headless backend issues).

Your task:
1. Debug and fix `/home/user/analyze.py` so it properly generates the `bootstrap_dist.png` histogram and the `/home/user/tracking.json` file.
2. Run the script to generate the artifacts.
3. Write and start a Python HTTP server (using Flask, FastAPI, or `http.server`) that listens on `0.0.0.0:8000`.
4. The server must implement the following endpoints:
   - `GET /api/tracking` : Returns the JSON content of `/home/user/tracking.json`.
   - `GET /api/plot` : Serves the generated `bootstrap_dist.png` image file.

Leave your server running in the background on port 8000 when you are finished.