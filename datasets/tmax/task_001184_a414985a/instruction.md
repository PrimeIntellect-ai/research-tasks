I am a researcher trying to organize a legacy dataset that was weirdly archived as an MP4 video. I need your help to reconstruct the original knowledge graph and build a query tool for it.

The video is located at `/app/dataset_video.mp4`. It encodes a directed graph. 
Each frame in the video represents a single directed edge. 
- The video is exactly 120 frames long (12 seconds at 10 fps).
- Each frame can be cleanly split into a left half and a right half.
- The uniform grayscale luminance (0-255) of the left half represents the Source Node ID.
- The uniform grayscale luminance (0-255) of the right half represents the Target Node ID.
- The video was encoded losslessly. If you extract the frames (e.g., by scaling to 2x1 pixels and extracting the grayscale values), the raw byte values of the 2 pixels correspond exactly to the `Source` and `Target` IDs.

Here is what I need you to do:
1. Extract the sequence of directed edges from `/app/dataset_video.mp4`. Save this extracted graph as `/home/user/edges.txt`, where each line contains `Source Target` (space-separated integers).
2. Write a C program `/home/user/query.c` that:
   - Reads the `/home/user/edges.txt` file on startup to build the graph in memory.
   - Reads routing queries from `stdin`. Each query is a single line containing two integers `U V`.
   - Computes the shortest directed path from `U` to `V` using Breadth-First Search.
   - If there are multiple shortest paths, it MUST break ties by choosing the path that is lexicographically smallest based on the sequence of Node IDs.
   - Outputs the path to `stdout` in the exact format: `Path: U->X->Y->V` followed by a newline.
   - If no path exists, output `NONE\n`.
   - Continues processing queries until EOF.
3. Compile your program to an executable at `/home/user/query`.

You may use standard Linux tools (like `ffmpeg`, `hexdump`, `awk`) to process the video and generate `edges.txt`. Do not use external libraries for the C program other than the standard C library.