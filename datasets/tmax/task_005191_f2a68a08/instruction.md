You are an AI assistant helping a manufacturing engineering team debug their automated configuration manager. 

The configuration manager receives updates via a secure optical diagnostic channel. We have a recording of the latest configuration broadcast in `/app/config_signal.mp4`. 
This video is exactly 32 frames long (encoded at 1 fps). Each frame is either completely black or completely white, representing a 32-bit unsigned integer broadcast in big-endian format (White = 1, Black = 0). 

Your task is to:
1. Extract the frames from `/app/config_signal.mp4` to decode this 32-bit unsigned integer, which represents the dynamic scaling factor `S`.
2. Write a C program (e.g., in `/home/user/process.c`) that parses a provided GCode file located at `/app/base_toolpath.gcode`. 
3. The GCode file contains linear movement commands in the format `G1 X<val> Y<val>`. You must parse these lines and apply a transformation macro to the toolpath using the scale factor `S`:
   - If a point's original X coordinate is less than 0, multiply BOTH its X and Y coordinates by `S`.
   - If a point's original X coordinate is greater than or equal to 0, multiply BOTH its X and Y coordinates by `(S / 2.0)`.
4. Calculate the total Euclidean travel distance of this newly transformed toolpath. 
   - Assume the tool head starts at `(0.0, 0.0)`.
   - Only process `G1` commands that explicitly contain both an `X` and a `Y` value. Ignore any other commands, blank lines, or comments.
   - Calculate the distance cumulatively from point to point.

Use shell commands (like `ffmpeg`) to process the video and extract the frames, and use **C** to write the GCode parsing and distance calculation logic. Compile and run your C program to find the final distance.

Save the final total calculated distance (as a plain floating-point number, e.g., `123456.78`) to the file `/home/user/total_distance.txt`.