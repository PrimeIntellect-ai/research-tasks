I am a researcher organizing and analyzing datasets from a recent physics experiment. The experiment's optical sensor produced a video file located at `/app/experiment.mp4`. The video records a flickering light source over 40 frames. I need you to build an automated ETL pipeline, perform time-series analysis, and expose the results via a Go-based web service. 

Please perform the following steps, writing your data processing and server code entirely in **Go** (you may use `ffmpeg` or other shell utilities to extract the data first):

1. **Data Extraction**: Extract the average grayscale brightness (0-255) of each frame in the video, in order from frame index 0 to 39.
2. **Missing Value & Outlier Handling**:
   - Camera glitches caused some frames to drop completely to `0` brightness. Treat any frame with an average brightness of exactly `0` as a missing value. Replace it using linear interpolation between the nearest previous and next valid (non-zero, non-outlier) frames.
   - External flashes caused outliers. Treat any frame with an average brightness `> 200` as an outlier. Replace it with the **median** of the exactly 5 preceding valid (cleaned) frames.
3. **Model Cross-Validation & Hyperparameter Tuning**:
   - We want to predict the next frame's brightness using a Simple Moving Average (SMA) of the previous $k$ frames.
   - Tune the hyperparameter $k$ by searching $k \in \{2, 3, 4, 5, 6\}$.
   - Use Time-Series Cross-Validation. Split the 40 cleaned frames sequentially into 4 equal folds of 10 frames each (Fold 1: indices 0-9, Fold 2: 10-19, etc.).
   - Perform 3 test splits: 
     - Train on Fold 1, Test on Fold 2.
     - Train on Folds 1+2, Test on Fold 3.
     - Train on Folds 1+2+3, Test on Fold 4.
   - For each test split, calculate the Mean Squared Error (MSE) of the predictions. The prediction for index `i` is the average of the `k` cleaned frames immediately preceding `i`.
   - Calculate the average of the 3 test MSEs for each $k$, and select the $k$ with the lowest average MSE.
4. **Service Integration**: Write and run a Go HTTP server listening on `0.0.0.0:8080` that serves the final results.
   - All endpoints must require the header `Authorization: Bearer RES-8821`. Return `401 Unauthorized` if missing or incorrect.
   - `GET /health` : Returns JSON `{"status": "ok"}`
   - `GET /optimal_k` : Returns JSON `{"k": <int>}` containing your optimal window size.
   - `GET /predict` : Returns JSON `{"prediction": <float>}` predicting the brightness of frame index 40, calculated using the optimal $k$ and the last $k$ cleaned frames (indices up to 39).

Run the server in the background so it remains active. Do not stop once it is running.