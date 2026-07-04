You are an AI assistant helping a computational researcher process an experiment that bridges visual spectroscopy and Monte Carlo graph simulations.

In the `/home/user/experiment` directory, you have a setup waiting for you. However, the data you need to process is located in a video file at `/app/particle_experiment.mp4`. 

Here is your multi-step task:

1. **Signal Processing on Video Data**:
   The video `/app/particle_experiment.mp4` (10 seconds, 30 fps) contains a visual recording of three simulated "particles" (nodes in a graph) that blink to indicate their energy levels. 
   - Node 0 is located exactly at coordinates (x=100, y=100).
   - Node 1 is located exactly at coordinates (x=300, y=100).
   - Node 2 is located exactly at coordinates (x=200, y=300).
   Use `ffmpeg`, `ImageMagick`, or other shell utilities to extract frames and compute the brightness of these specific locations over time. Count the total number of distinct "blinks" (peak brightness events) for each node over the entire 10 seconds. Let these blink counts be $f_0$, $f_1$, and $f_2$.

2. **Software Compilation**:
   There is a C source file `/home/user/experiment/mc_sim.c` that performs a Monte Carlo simulation of a particle network based on energy frequencies. 
   Compile this C file into an executable named `mc_sim` in the same directory. You may use `gcc` (which is pre-installed).

3. **Service Configuration (Bash)**:
   Write a Bash script at `/home/user/experiment/server.sh`. This script must:
   - Act as a simple HTTP server listening on TCP port 8080 (you may use `socat`, `nc`, or standard bash networking).
   - When it receives an HTTP `GET /simulate` request, it must run your compiled Monte Carlo simulation using the counts you discovered: `./mc_sim $f_0 $f_1 $f_2`.
   - The server must return a valid `HTTP/1.1 200 OK` response. The body of the response must be *exactly* the stdout produced by the `mc_sim` executable.
   - Run this server in the background so it is actively listening.

**Constraints & Notes**:
- You must use Bash for the `server.sh` script.
- Ensure the server stays running and can handle at least one request from an automated verifier.
- The verifier will make a standard HTTP GET request to `http://localhost:8080/simulate`.