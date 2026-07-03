You are a data analyst tasked with building an ETL and inference pipeline entirely in Bash and standard GNU Unix tools. We need to process a video file to detect anomalous frames (e.g., camera glitches) using a pre-trained linear model. 

Here is your objective:

1. **Feature Extraction**: 
   Analyze the video located at `/app/video.mp4`. Use `ffmpeg` to extract frame-level statistics using the `signalstats` filter. Specifically, you need to extract the average luma value (`YAVG`) and the average saturation (`SAVG`) for every frame.
   
2. **Data Processing (ETL)**:
   Parse the output of `ffmpeg` to create a structured CSV dataset. The dataset should have the header `frame_num,YAVG,SAVG`, where `frame_num` starts at 1 for the first frame.

3. **Model Inference Engine**:
   We have a pre-trained logistic regression model. The weights are:
   - W_Y (weight for YAVG) = 0.15
   - W_S (weight for SAVG) = -0.08
   - Bias (B) = -12.5
   
   Write a script using standard command-line tools (like `awk`, `bash`, or `bc`) to reconstruct this model's forward pass. For each frame, compute the raw score `Z = (W_Y * YAVG) + (W_S * SAVG) + B`. 
   Then, compute the anomaly probability using the sigmoid function: `P = 1 / (1 + exp(-Z))`. 

4. **Output Generation**:
   Save the final predictions to `/home/user/predictions.csv`. 
   The file must have exactly this format:
   ```csv
   frame_num,probability
   1,0.00245
   2,0.00312
   ...
   ```
   Ensure your probabilities are printed with at least 5 decimal places.

Your pipeline should process the entire video and output the final CSV. An automated test will evaluate the Mean Squared Error (MSE) of your probabilities against a reference implementation. Your MSE must be strictly less than 0.0001.