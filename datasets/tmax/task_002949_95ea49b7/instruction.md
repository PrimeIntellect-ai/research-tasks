You are acting as a performance engineer profiling a new distributed mesh refinement simulation. During large-scale runs, a thread synchronization bug causes the domain decomposition state to become corrupted.

We have captured a video of the simulation's visual output during a test run, located at `/app/simulation_run.mp4`. 
Normally, the video shows the mesh domain as a grayscale grid. When the synchronization glitch occurs, it results in a highly visible anomaly: a bright, saturated red horizontal band across the visualization (where the red channel heavily dominates).

Your task is to build a detector to filter out these corrupted frames from our experimental data pipelines.

1. Use `ffmpeg` (or any tool) to extract and reshape the observational frame data from `/app/simulation_run.mp4` to understand the visual profile of the normal vs. glitch states.
2. Write a Python script located at `/home/user/detect_glitch.py`.
3. The script must accept exactly one argument: the path to an image file. 
   Example: `python3 /home/user/detect_glitch.py frame_001.png`
4. The script must print exactly `GLITCH` to standard output if the frame exhibits the red band anomaly, and `CLEAN` if it is a normal mesh refinement frame.

Your script will be tested against a massive, separate corpus of clean and corrupted frames.