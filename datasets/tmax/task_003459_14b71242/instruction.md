You are an ML engineer tasked with preparing a clean dataset of video frames for training. Unfortunately, the source video contains sporadic corrupted "glitch" frames that will ruin the training process.

We have provided a pre-trained autoencoder model that was trained exclusively on clean frames. You can use its reconstruction error to detect anomalies (corrupted frames).
The model weights are located at `/app/ae_weights.pth`.

The Autoencoder architecture is as follows (PyTorch):
- **Encoder**: `Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=2, padding=1)` followed by a `ReLU` activation.
- **Decoder**: `ConvTranspose2d(in_channels=16, out_channels=3, kernel_size=3, stride=2, padding=1, output_padding=1)` followed by a `Sigmoid` activation.
- The model expects inputs as PyTorch tensors of shape `(1, 3, 64, 64)` with values in the range `[0, 1]`.

Your task consists of three parts:

1. **Create a Detector**: Write a Python script at `/home/user/detector.py` that takes a single image file path as a command-line argument. The script must:
   - Load the image and resize it to 64x64 pixels.
   - Convert it to a PyTorch tensor (scaled to [0, 1]).
   - Pass it through the reconstructed autoencoder.
   - Calculate the Mean Squared Error (MSE) between the input and the reconstructed output.
   - Classify the image as "clean" or "corrupted" based on a threshold.
   - **Exit with status code 0 if the image is clean.**
   - **Exit with status code 1 if the image is corrupted.**
   - Ensure the script is executable and starts with `#!/usr/bin/env python3`.

2. **Calibrate the Threshold**: We have provided two datasets of images for you to find the perfect MSE threshold:
   - Clean examples: `/app/corpora/clean/`
   - Corrupted examples: `/app/corpora/evil/`
   Your `detector.py` must achieve 100% accuracy on these folders (exit 0 for all clean, exit 1 for all evil).

3. **Process the Unlabeled Video**: 
   - Extract frames from the video located at `/app/unlabeled_video.mp4` at exactly **1 frame per second (1 fps)** using `ffmpeg`. Save them as PNG images in `/home/user/frames/` using the naming format `%03d.png` (e.g., `001.png`, `002.png`).
   - Run your `detector.py` on every extracted frame.
   - Create a text file at `/home/user/clean_frames.txt` containing the filenames (just the filename, e.g., `004.png`) of all frames identified as clean. Write one filename per line, sorted alphabetically.

Make sure your numerical library configurations and inference code are correct to prevent false positives.