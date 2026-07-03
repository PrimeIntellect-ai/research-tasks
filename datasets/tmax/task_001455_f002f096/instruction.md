I need you to prepare some training data from a video file and serve it via a local API for our modeling pipeline.

We have a video artefact located at `/app/data/training_video.mp4`. You must act as a Machine Learning Engineer and complete the following steps using Bash and Python:

1. **Frame Extraction (Feature Engineering):**
   Write a Bash script named `/home/user/extract.sh` that uses `ffmpeg` to extract exactly 1 frame per second from `/app/data/training_video.mp4`. Save these frames as JPEG images in `/home/user/frames/` with the naming convention `frame_000.jpg`, `frame_001.jpg`, etc.

2. **Embedding Computation:**
   We are using a lightweight, deterministic baseline "embedding" for this phase. Write a Python script `/home/user/compute_embeddings.py` that processes all extracted frames. For each frame, load the image, convert it to standard Grayscale (using PIL's `.convert('L')`), and compute an 8-bin histogram of the pixel intensities (bins: 0-31, 32-63, ..., 224-255). Normalize this histogram so that the sum of the bins equals 1.0. Round each bin value to 4 decimal places.
   Save the output to `/home/user/embeddings.json` as a dictionary mapping the integer frame ID (e.g., `0`, `1`, `2`) to its 8-element list.

3. **Data Serving (API):**
   Stand up a local HTTP API to serve this data and a helper tokenizer. Create and start a Python web server (e.g., using Flask or FastAPI) listening exactly on `127.0.0.1:8888`. It must remain running in the background.

   The API must support these two endpoints:
   - `GET /api/embedding?id=<integer>`
     Returns a JSON response: `{"id": <integer>, "embedding": [val1, val2, ..., val8]}` based on the data in `embeddings.json`. If the ID does not exist, return a 404.
   - `POST /api/tokenize`
     Accepts a JSON payload like `{"text": "Sample text for tokenization!"}`.
     Returns a JSON response: `{"tokens": ["sample", "text", "for", "tokenization"]}`. 
     The tokenization logic should simply lowercase the text, remove all non-alphanumeric characters (except spaces), and split by whitespace.

Run your scripts so the frames are extracted, the `embeddings.json` is generated, and the HTTP service is actively listening on port 8888.