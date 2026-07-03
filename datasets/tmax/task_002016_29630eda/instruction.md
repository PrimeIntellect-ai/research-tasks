You are an AI assistant helping a data science researcher organize and analyze a video dataset. The researcher wants to track the occurrence of a specific visual event in a long video by building a reproducible pipeline that extracts frames, computes deep embeddings, and applies a Bayesian Hidden Markov Model (HMM) to infer the probability of the event occurring over time.

Your objective is to build this pipeline and compute the marginal posterior probability of the event for every second of the video.

Here are your instructions:

1. **Frame Extraction**:
   There is a video file located at `/app/data.mp4`. 
   Create a directory `/home/user/frames/`. Use `ffmpeg` to extract frames from the video at exactly 1 frame per second (FPS). Name the frames `frame_%04d.jpg` (e.g., `frame_0001.jpg`, `frame_0002.jpg`, etc.).

2. **Feature Engineering (Embeddings)**:
   Write a Python script to compute embeddings for each extracted frame. 
   - Use PyTorch and `torchvision.models.resnet18(pretrained=True)`.
   - Remove the final fully connected layer (or use the output of `AdaptiveAvgPool2d` flattened to a 512-dimensional vector).
   - Before passing frames through the model, resize them to 224x224, convert to RGB tensors, and normalize using standard ImageNet statistics (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]).
   - Set the model to evaluation mode (`.eval()`).

3. **Similarity & Likelihood (Emission Model)**:
   The "target" event is perfectly represented by the frame at exactly 15 seconds (i.e., `frame_0015.jpg`). Let this target embedding be $A$.
   For every frame $t$ (including the target itself), compute the cosine similarity $S_t$ between the frame's embedding $x_t$ and the target embedding $A$.
   
   We define a two-state system: State 1 (Event Present) and State 0 (Event Absent).
   Define the unnormalized observation likelihoods for each frame as:
   - $L(x_t \mid \text{State} = 1) = \exp(5 \times S_t)$
   - $L(x_t \mid \text{State} = 0) = \exp(2.0)$

4. **Bayesian Inference (HMM)**:
   Apply the Forward-Backward algorithm to compute the marginal posterior probability $P(\text{State}_t = 1 \mid x_{1:T})$ for all frames.
   Use the following HMM parameters:
   - Initial probabilities: $P(\text{State}_1 = 1) = 0.1$, $P(\text{State}_1 = 0) = 0.9$
   - Transition probabilities:
     - $P(\text{State}_t = 1 \mid \text{State}_{t-1} = 1) = 0.9$
     - $P(\text{State}_t = 0 \mid \text{State}_{t-1} = 1) = 0.1$
     - $P(\text{State}_t = 1 \mid \text{State}_{t-1} = 0) = 0.05$
     - $P(\text{State}_t = 0 \mid \text{State}_{t-1} = 0) = 0.95$

5. **Reporting**:
   Save the final marginal posterior probabilities to `/home/user/posteriors.csv`. 
   The CSV must have exactly two columns: `frame_name` (e.g., `frame_0001.jpg`) and `posterior_prob` (a float between 0 and 1 representing $P(\text{State}_t = 1 \mid x_{1:T})$).
   Ensure the rows are sorted alphabetically by `frame_name`.

Note: You should create a main bash script or Makefile that runs this entire reproducible pipeline from start to finish. Ensure all Python dependencies like `torch`, `torchvision`, and `Pillow` are installed in your environment before running.