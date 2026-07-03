You are a data analyst for an industrial manufacturing plant. You have been tasked with building a robust data pipeline that extracts telemetry from video feeds and sanitizes incoming CSV logs by identifying malicious or corrupted data.

Your task has two parts:

**Part 1: Video Data Extraction**
You are provided with a video file of a machine monitor at `/app/machine_monitor.mp4`. 
1. Use Python (with `cv2` or `ffmpeg`) to extract the average grayscale brightness (0-255) of every frame in the video.
2. Save this data to `/home/user/video_telemetry.csv`. The CSV must have exactly two columns: `frame_index` (starting at 0) and `brightness` (float, rounded to 2 decimal places).

**Part 2: Adversarial CSV Sanitization**
We frequently receive CSV logs containing `temperature` and `pressure` readings. Valid (clean) machinery data strictly follows a specific statistical relationship: `pressure` is linearly dependent on `temperature` ($pressure = \beta \cdot temperature + \alpha + \epsilon$), where $\epsilon$ is Gaussian noise with a known, small variance. Malicious or corrupted (evil) data deviates from this relationship (e.g., the slope $\beta$ or intercept $\alpha$ is significantly different, or the noise variance is completely wrong).

We have provided a training corpus to help you understand the distributions:
- Clean samples: `/app/corpus/train/clean/`
- Corrupted samples: `/app/corpus/train/evil/`

Your objective is to write a Python script at `/home/user/classifier.py` that can classify any given CSV log.
- **Signature:** The script must accept exactly one argument (the path to the CSV file): `python3 /home/user/classifier.py <path_to_csv>`
- **Output:** The script must perform statistical hypothesis testing or numerical accuracy checks (e.g., linear regression, checking confidence intervals for the slope/intercept) and print exactly `CLEAN` or `EVIL` to standard output.

To succeed, your `classifier.py` must perfectly classify a hidden evaluation corpus without relying on hardcoded filenames or row counts.