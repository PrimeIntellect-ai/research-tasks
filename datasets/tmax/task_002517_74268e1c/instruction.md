You are a performance engineer analyzing the rendering pipeline of a new application. To measure the true update rate of the display pipeline, we recorded a high-speed video of a diagnostic UI element (a flashing square). 

You have been provided with a video artifact at `/app/ui_render_test.mp4`. The video is recorded at 60 FPS. The diagnostic square is located in the top-left 100x100 pixels of the video.

Your task is to build a reproducible, automated Bash pipeline that extracts the average luminance (brightness) of this region over time and computes the dominant frequency (in Hz) of its flashing using a Fast Fourier Transform (FFT).

To complete this task, you must build the entire pipeline and output the final result.

Specific requirements:
1. **Scientific Environment Management**: Create a Python virtual environment at `/home/user/perf_env` and install any necessary numerical libraries (e.g., `numpy`, `scipy`) required for your spectral analysis.
2. **Observational Data Reshaping**: Write a Bash script `/home/user/extract_signal.sh` that uses `ffmpeg` to crop the top-left 100x100 region of `/app/ui_render_test.mp4`, extracts the average luminance (Y channel) for each frame, and reshapes this data into a clean CSV format with columns: `Frame,Luminance`.
3. **Spectral Analysis**: Write a Python script `/home/user/fft_analyzer.py` that reads the CSV, computes the FFT of the luminance signal assuming a 60 Hz sampling rate, and identifies the dominant frequency (ignoring the 0 Hz / DC component).
4. **Reproducible Pipeline**: Write a master Bash script `/home/user/run_pipeline.sh` that ties it all together: activates the environment, runs the extraction, runs the analysis, and saves ONLY the numerical dominant frequency (as a float in Hz) to `/home/user/dominant_frequency.txt`.

Run your pipeline to generate the final `/home/user/dominant_frequency.txt` file. Your output will be graded by an automated verifier that checks how close your computed frequency is to the true hardware rendering frequency.