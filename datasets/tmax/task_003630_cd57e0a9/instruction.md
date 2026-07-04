I am a researcher organizing a hybrid dataset that consists of manufacturing trajectories embedded within audio memos. 

I have an audio file located at `/app/dataset_record.wav`. The spoken content of this audio file dictates a specific integer byte offset. 

Your tasks are to:
1. Determine the spoken byte offset from the audio file.
2. Write a C++ program (saved to `/home/user/extractor.cpp`) that reads `/app/dataset_record.wav` as a binary file, seeks to that exact byte offset, and extracts an embedded ELF executable file that has been appended there.
3. The embedded ELF file contains a custom section named `.gcode` which holds a large plaintext GCode dataset. Extract this GCode text.
4. Parse the extracted GCode to calculate the total 2D distance of the toolpath. Only consider `G1` commands that contain both `X` and `Y` coordinates. The toolpath starts at `(0, 0)`. The distance is the sum of the Euclidean distances between consecutive `(X, Y)` points in these `G1` commands.
5. Save the final calculated total distance as a floating-point number (rounded to 2 decimal places) to `/home/user/distance_metric.txt`.

You can use any standard command-line tools available in a typical Linux environment (e.g., Python whisper/ffmpeg packages for transcription, `objcopy` or `readelf` for ELF extraction) alongside your C++ code.