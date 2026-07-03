You are acting as a data scientist analyzing experimental data from a time-resolved spectroscopy experiment. The raw data is provided as a video file at `/app/reaction_spectroscopy.mp4`. 

The video displays a single bright peak representing the emission maximum of a chemical reaction over time. The peak's position on the x-axis (in pixels) corresponds to the emission wavelength. As the reaction proceeds, the peak shifts horizontally. Theoretical models suggest that the position of the peak $x(t)$ follows an exponential decay model:
$$x(t) = A \cdot \exp(-k \cdot t) + C$$
where $t$ is the frame index (starting at $t=0$ for the first frame), $A$ is the amplitude, $k$ is the decay constant, and $C$ is the baseline position.

Your task is to:
1. Extract the frames from `/app/reaction_spectroscopy.mp4` (you may use `ffmpeg`).
2. Write a script (using Bash, Python, or a combination) to find the x-coordinate of the brightest pixel in each frame.
3. Fit the exponential decay model to the extracted coordinates $(t, x(t))$ to determine the decay constant $k$.
4. Output ONLY the estimated decay constant $k$ (as a floating-point number) to a file located at `/home/user/decay_constant.txt`.

The accuracy of your estimated $k$ will be evaluated programmatically against the ground truth.