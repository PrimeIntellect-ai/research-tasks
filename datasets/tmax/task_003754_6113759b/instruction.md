You are an ML Engineer tasked with preparing training data from a raw video and setting up an API to serve extracted features and a baseline classification model. 

There is a video file located at `/app/sample_video.mp4`. 

Please perform the following steps:
1. **Analysis Environment Setup:**
   Install necessary packages in your Python environment. You will likely need `opencv-python-headless`, `scikit-learn`, `fastapi`, `uvicorn`, and `pydantic`.

2. **Video Feature Extraction:**
   Read `/app/sample_video.mp4`. Extract exactly one frame for every second of the video (i.e., at timestamp 0.0s, 1.0s, 2.0s, etc., up to the total integer duration). 
   For each extracted frame, convert it to grayscale and calculate the mean pixel intensity as a float. 
   Define a boolean label `is_bright` which is `True` if the mean intensity is >= 120.0, and `False` otherwise.

3. **Classification Model:**
   Using `scikit-learn`, train a `LogisticRegression` model (with `random_state=42` and default parameters) to predict `is_bright` based solely on the `frame_index` (where frame at 0.0s is index 0, 1.0s is index 1, etc.). Note: `frame_index` should be treated as a 2D array of shape `(n_samples, 1)` for sklearn.

4. **API Service and Schema Enforcement:**
   Create a FastAPI application and run it on `127.0.0.1:8000` (it must stay running in the background or you can start it as the final blocking command).
   All endpoints must enforce strict authorization via an HTTP Bearer token: `Bearer ml-data-token-999`. Requests without this exact token must return a 401 or 403 status code.

   The API must expose two endpoints:
   - `GET /features`
     Returns a JSON list of the extracted frame data. 
     Response Schema (list of objects): `{"frame_index": int, "mean_intensity": float, "is_bright": bool}`

   - `POST /predict`
     Accepts a JSON payload strictly enforcing this schema: `{"frame_index": int}`
     Returns the model's prediction for that frame index.
     Response Schema: `{"predicted_is_bright": bool}`

Ensure your code is clean and properly handles the video boundaries. Do not hardcode the number of frames; derive it from the video length.