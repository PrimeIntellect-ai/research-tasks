You are a Machine Learning Engineer tasked with preparing probabilistic training targets based on video data. We have a pipeline that relies on a C-based backend to serve data schema-compliant targets for downstream model training.

Your task consists of the following steps:

1. **Extract Video Frames**:
   We have a video file located at `/app/input.mp4`. Use `ffmpeg` to extract all frames from this video into the directory `/home/user/frames/`.
   - Scale the output to 64x64 pixels.
   - Convert them to grayscale.
   - Save them as PGM format (P5, binary), named as `frame_%03d.pgm` (e.g., `frame_001.pgm`, `frame_002.pgm`).

2. **Simulate Pipeline Data Loss (Schema Enforcement)**:
   In our real pipelines, integer keys often silently drop, behaving like NaNs. To simulate this and enforce robust handling in your backend, delete every frame whose numerical ID is a multiple of 5 (e.g., `frame_005.pgm`, `frame_010.pgm`, etc.).

3. **Implement Bayesian Target Server**:
   Write a C program at `/home/user/serve_targets.c` and compile it to `/home/user/serve_targets`. The program must act as a TCP server listening on `127.0.0.1:8080`.

   When a client connects, it will send a frame number followed by a newline (e.g., `4\n`). 
   Your server must:
   - Attempt to open the corresponding PGM file.
   - If the file is missing (the schema has a 'NaN' hole), the server must respond exactly with `NaN\n`.
   - If the file exists, calculate the arithmetic mean of all 4096 pixel values in that frame (let this be $x_i$, a float).
   - We are updating our prior belief of frame brightness. Calculate the posterior mean assuming a Gaussian distribution:
     - Prior Mean ($\mu_0$): 128.0
     - Prior Variance ($\sigma_0^2$): 50.0
     - Observation Variance ($\sigma^2$): 10.0
     - The formula for the posterior mean is: 
       $$ \mu_{post} = \frac{\frac{\mu_0}{\sigma_0^2} + \frac{x_i}{\sigma^2}}{\frac{1}{\sigma_0^2} + \frac{1}{\sigma^2}} $$
   - Send the posterior mean back to the client formatted to exactly two decimal places, followed by a newline (e.g., `124.32\n`).
   - Close the client connection after sending the response, but keep the server running to accept the next connection.

Start your server in the background so the testing framework can query it.