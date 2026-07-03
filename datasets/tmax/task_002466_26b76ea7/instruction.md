Hello! I am a data analyst working on processing sensor logs from our manufacturing line. I need you to write a C++ program that correlates log data from a CSV with a video feed to produce a smoothed analytical output. 

I have a calibration video located at `/app/calibration.mp4`. It is exactly 100 frames long. 
First, you need to analyze this video and extract a "calibration weight" for each frame index (0 to 99). 
The calibration weight $W_i$ for frame $i$ is defined as the sum of all grayscale pixel intensities in frame $i$, modulo 256. You can use `ffmpeg` to extract the frames as grayscale images or process it however you like.

Once you know the weights, I need a C++ CLI tool located at `/home/user/analyzer`. 
This tool must accept a single argument: the path to a CSV file.

The input CSV has no header and contains three columns:
`frame_index` (integer, 0 to 99)
`node_id` (string, e.g., "SensorA")
`value` (float)

Your C++ program must do the following:
1. Parse the input CSV.
2. Group the data by `node_id`.
3. For each `node_id`, order the rows by `frame_index` in ascending order.
4. Calculate a sliding window sum. For the current row, the smoothed value is the sum of `(value * W_{frame_index})` for the current row and up to 2 preceding rows *for that specific node_id* (i.e., a window size of 3 rows).
5. Print the results to standard output in the exact format: `frame_index,node_id,smoothed_value` (with `smoothed_value` formatted to exactly 2 decimal places, e.g., `45,SensorA,1234.50`). The output rows must be sorted by `node_id` (alphabetically) and then by `frame_index` (ascending).

The C++ tool must be compiled and ready to execute at `/home/user/analyzer`. It must be highly performant and handle missing frame sequences (e.g., if a node has data for frames 2, 5, and 10, the window for frame 10 uses the rows from 2, 5, and 10). 
Do not hardcode the input CSV path; it will be passed as the first command-line argument.

Please set everything up and compile the final binary.