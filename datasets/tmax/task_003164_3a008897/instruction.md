You are an ML engineer preparing training data and an inference service for a video frame recommendation system. 

We have a short video located at `/app/test_video.mp4`. Your objective is to extract features from its frames, carefully normalize them without data leakage, and serve similarity recommendations over an HTTP API.

Here are the specific requirements:

1. **Frame Extraction**:
   Use `ffmpeg` to extract frames from `/app/test_video.mp4` at exactly 1 frame per second. Save them as PNG images in `/home/user/frames/` with the naming convention `frame_1.png`, `frame_2.png`, etc.

2. **Feature Extraction**:
   Write a Python script to compute exactly 6 features for each extracted frame in order:
   - Mean of the Red channel
   - Mean of the Green channel
   - Mean of the Blue channel
   - Standard deviation of the Red channel
   - Standard deviation of the Green channel
   - Standard deviation of the Blue channel
   *(Use standard libraries like `Pillow` and `numpy` to compute these).*

3. **Data Normalization (Avoid Data Leakage)**:
   Sort the frames by their ID (1, 2, 3...). 
   Split the data conceptually: the first half of the frames (IDs from 1 up to `N // 2`, where N is the total number of extracted frames) form the "train" set. The rest form the "test" set.
   Standardize all 6 features to have zero mean and unit variance. **Important**: You must fit your scaler (compute the means and standard deviations for normalization) **strictly on the train set**. Then apply this scaler to transform all frames (both train and test).

4. **Recommendation API**:
   Write and start a Python HTTP server (e.g., using `Flask` or `http.server`) that listens on `127.0.0.1:8080`. It must serve two endpoints:
   
   - `GET /stats`: Returns a JSON response with the means used for normalization. 
     Format: `{"train_means": [mean1, mean2, mean3, mean4, mean5, mean6]}` (floats rounded to 2 decimal places).
     
   - `GET /recommend?frame_id=<X>`: Computes the Euclidean distance between the scaled features of `frame_id=<X>` and all other frames. Returns a JSON response containing the integer IDs of the top 3 most similar frames (smallest distance), excluding the queried frame itself.
     Format: `{"recommendations": [id1, id2, id3]}`

Start your server as a background process so it continues running. Ensure it binds to `127.0.0.1:8080`.