You are an automation specialist creating a video analysis workflow. Your goal is to process a video, extract color features, and compute the similarity between consecutive frames using a custom C program.

We have a video file located at `/app/video.mp4`. 

First, write a C program that reshapes wide-format RGB data into long-format distance data. 
Save your code to `/home/user/calc_similarity.c` and compile it to `/home/user/calc_similarity`.
Requirements for the C program:
- It should read from standard input line by line.
- Each line will contain a space-separated list of integers representing consecutive RGB colors: `R0 G0 B0 R1 G1 B1 R2 G2 B2 ...`
- If the number of integers on a line is not a multiple of 3, the program should silently ignore that line and proceed to the next.
- For each valid line, the program must compute the Euclidean distance between adjacent frame colors (i.e., Frame 0 and Frame 1, Frame 1 and Frame 2, etc.).
- The output should be printed to standard output in the following long format:
  `[Index1] [Index2] [R1] [G1] [B1] [R2] [G2] [B2] [Distance]`
  where `Distance` is the Euclidean distance formatted to exactly two decimal places (e.g., `%.2f`).
- Frame indices start at 0 for each line.
- Example input: `10 20 30 10 20 30 40 20 70`
- Example output:
  `0 1 10 20 30 10 20 30 0.00`
  `1 2 10 20 30 40 20 70 50.00`

Second, write a bash script `/home/user/pipeline.sh` that orchestrates this workflow:
1. Extracts frames from `/app/video.mp4` at exactly 1 frame per second.
2. Computes the average RGB color of each frame (hint: resizing to 1x1 pixel is a fast way to get the average color).
3. Writes all the extracted RGB values as a single space-separated line (wide format) into `/home/user/rgb_wide.txt` in chronological order.
4. Streams the contents of `/home/user/rgb_wide.txt` into your compiled `/home/user/calc_similarity` program.
5. Saves the final output to `/home/user/distances.txt`.

Make sure `/home/user/pipeline.sh` is executable and run it to generate the final files.