You are an AI assistant helping a performance engineer profile a UI application's responsiveness. We have screen recordings of a UI element that is supposed to pulsate exactly at 10 Hz. When the system is under heavy load, the UI thread stalls, causing stuttering and irregular update intervals.

Your task is to create a Python classifier that can automatically analyze these video recordings and detect whether the UI is running smoothly ("CLEAN") or stuttering ("EVIL").

Specifically, you need to write a script at `/home/user/detect_stutter.py` that takes a single command-line argument (the path to an `.mp4` video file). The script must output EXACTLY the string "CLEAN" or "EVIL" on a single line to standard output, with no other text.

The videos are recorded at 30 FPS. The pulsating UI element is located in the center of the video. To build your classifier, you must:
1. Extract the frames using `ffmpeg` or `OpenCV` (pre-installed).
2. Reshape the observational data: calculate the average grayscale brightness of the center 50x50 pixel region over time to create a 1D time-series signal.
3. Perform a Fourier transform (FFT) on this time-series to obtain the spectral power distribution.
4. Calculate a probability distribution distance metric (e.g., Wasserstein distance) between the normalized power spectrum of the video and the "ideal" spectrum (which has a single sharp peak at 10 Hz).
5. Implement convergence testing: rather than processing the entire video at once, compute the distance metric on progressively larger time windows (e.g., starting with 1 second, then 2 seconds, etc.). Stop and make a classification decision once the metric converges (changes by less than 5% between steps), to save processing time.

We have provided a sample video at `/app/test_fixture.mp4` that you can use to develop your logic (it is an example of an "EVIL" stuttering video).

Once you have written your script, an automated test suite will evaluate it against a hidden adversarial corpus of videos. Your script must correctly classify 100% of the "clean" videos (smooth 10Hz) as CLEAN, and 100% of the "evil" videos (stuttering/jittery) as EVIL.