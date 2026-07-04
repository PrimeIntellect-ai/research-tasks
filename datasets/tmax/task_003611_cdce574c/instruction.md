As a deployment engineer rolling out the new audio processing pipeline, we need to deploy a custom C application that processes incoming audio instructions. 

Currently, we have an audio file located at `/app/input.wav`. This file is a standard 16-bit PCM mono WAV file (44100 Hz). 

Your task is to:
1. Write a C program at `/home/user/processor.c` that reads this WAV file, parses the header, and scales the amplitude of all audio samples by exactly 0.5 (halving the volume).
2. The program must write the resulting audio to a valid WAV file at `/home/user/output.wav`, maintaining the original WAV header format but with the modified sample data.
3. Compile the C program and run it to generate the output file.
4. Create a bash script at `/home/user/deploy.sh` that compiles the C code and processes the audio file automatically.
5. Set up a local Python-based web server on port 8080 serving the directory `/home/user` so the output can be downloaded, and log the web server's PID to `/home/user/server.pid`.

Please ensure your C program correctly handles the 44-byte WAV header and iterates through the 16-bit integer samples, multiplying each by 0.5. 

The final output `/home/user/output.wav` will be evaluated based on the Mean Squared Error (MSE) compared to our reference processed file.