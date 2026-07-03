You are an experimental data scientist working on a novel laser spectroscopy setup. Your detection apparatus doesn't produce standard arrays; instead, it outputs an raw video feed of a luminescent sensor element as the laser sweeps across a frequency range. 

You have been provided with an experimental recording at `/app/experiment_feed.mp4`.
The video consists of exactly 100 frames. The background is black, and the entire frame's mean pixel intensity represents the absorption signal $I$ at a given frequency. 

The laser frequency $\omega$ (in THz) sweeps linearly with the frame index $k$ (where $k=0$ is the first frame, up to $k=99$), according to the relation:
$$\omega_k = 100 + 5k$$

The extracted spectrum $I(\omega)$ contains two overlapping absorption peaks that conform to a double-Lorentzian profile with a constant baseline offset:
$$I(\omega) = \frac{A_1 \Gamma_1^2}{(\omega - \omega_1)^2 + \Gamma_1^2} + \frac{A_2 \Gamma_2^2}{(\omega - \omega_2)^2 + \Gamma_2^2} + C$$

Your task is to:
1. Extract the mean intensity of each frame from `/app/experiment_feed.mp4` to reconstruct the $I(\omega)$ dataset.
2. Use non-linear equation solving to fit the dataset to the double-Lorentzian model described above.
3. Determine the center frequencies $\omega_1$ and $\omega_2$ of the two peaks (where $\omega_1 < \omega_2$).
4. Expose the results by starting an HTTP server that listens on `127.0.0.1:8000`.
5. The server must have an endpoint `GET /api/peaks` that returns a JSON response containing the two fitted center frequencies rounded to 1 decimal place. The exact JSON format must be:
   `{"omega_1": 123.4, "omega_2": 567.8}`

You may install any necessary Python packages (like `opencv-python-headless`, `scipy`, `numpy`, `flask`, or `fastapi`) to accomplish this. Keep the web service running in the background or foreground so that it can be queried.