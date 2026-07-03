You are helping a researcher organize and validate a dataset extracted from a faulty video sensor. The video feed occasionally cuts out, producing completely black frames (missing values/outliers). 

Your task is to analyze the video, perform a Bayesian inference step to determine the probability that the sensor was "active" for each frame, and serve these probabilities via a C++ TCP server.

**Step 1: Data Extraction & Outlier Detection**
1. A video file is located at `/app/sensor_feed.mp4`. Extract the frames from this video using `ffmpeg` (e.g., to `/home/user/frames/` as PNGs or JPEGs).
2. Write a C++ program that reads each frame and computes the average grayscale pixel intensity (sum of all pixel values divided by the number of pixels, where RGB to grayscale is `0.299*R + 0.587*G + 0.114*B`).

**Step 2: Bayesian Inference**
Implement a Bayesian filter in your C++ program to compute the posterior probability that the sensor is "Active" given the average intensity $x$ of a frame.
- **Prior probability**: $P(Active) = 0.85$
- **Likelihood of intensity if Active**: $P(x | Active)$ follows a Normal distribution $\mathcal{N}(\mu=110.0, \sigma=30.0)$.
- **Likelihood of intensity if Inactive**: $P(x | Inactive)$ follows a Normal distribution $\mathcal{N}(\mu=0.0, \sigma=2.0)$.

Calculate the posterior probability $P(Active | x)$ for each frame index (0-indexed). Use standard numerical libraries or `<cmath>` to implement the Gaussian probability density function (PDF). Validate your model outputs to ensure probabilities are between 0 and 1.

**Step 3: Service Configuration**
Create a C++ TCP server that listens on `127.0.0.1:9090`. 
The server must accept incoming TCP connections and respond to the following newline-terminated (`\n`) text commands:
- `FRAME <N>\n`: Where `<N>` is an integer frame index. The server must respond with the computed posterior probability for that frame formatted exactly as: `PROB: <float>\n` (where `<float>` is rounded to 4 decimal places, e.g., `PROB: 0.9921`).
- `COUNT_INACTIVE\n`: Respond with the total number of frames where $P(Active | x) < 0.5$, formatted exactly as `INACTIVE: <integer>\n`.

Compile your C++ code (you may use `g++` and any standard library headers) and run the server in the background so it is listening on port 9090 when you finish the task.