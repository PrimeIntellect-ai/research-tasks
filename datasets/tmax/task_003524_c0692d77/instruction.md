You are a storage administrator managing a legacy server where voice recordings are taking up too much disk space. You need to implement an aggressive, custom compression strategy by removing absolute silence from uncompressed WAV files before archiving them.

Your task is to write a C++ program that reads an uncompressed PCM 16-bit Mono WAV file, removes silent audio frames (samples whose absolute amplitude falls below a certain threshold for a continuous duration), and writes the modified audio back to a new valid WAV file.

Here is the environment and requirements:
1. An audio recording is located at `/app/voicemail.wav`.
2. A configuration archive is at `/app/config_data.tar.gz`. Extract it to find `settings.ini`, which contains the noise floor threshold and minimum silence duration to trim. Use standard text tools (sed/awk) to extract these values and feed them to your program.
3. Write a C++ program (`/home/user/silence_trimmer.cpp`) that:
   - Parses the WAV header of the input file.
   - Iterates through the audio samples.
   - Drops contiguous blocks of samples that fall below the amplitude threshold (from the config) if the block duration exceeds the minimum silence duration.
   - Writes the remaining samples to a new WAV file, ensuring the RIFF/WAV header is updated with the correct new file size and data chunk size.
4. Compile your program and run it on `/app/voicemail.wav` to produce `/home/user/optimized.wav`.
5. Finally, create an archive `/home/user/final_storage.tar.gz` containing your `optimized.wav` and the extracted `settings.ini`.

The goal is to reduce the file size of the audio file as much as possible without distorting or losing any spoken words. An automated verifier will transcribe your `optimized.wav` using a standard Whisper model and compare it to the original transcript, while also measuring the disk space saved.