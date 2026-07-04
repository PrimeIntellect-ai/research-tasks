You are a Site Reliability Engineer monitoring a voice-activated alert system for an on-call NOC. Recently, a severe intermittent failure has been crashing the service. A legacy audio normalization service gets stuck in an infinite loop (convergence failure) when processing certain incoming audio alerts, causing CPU spikes and dropping critical alerts.

We have managed to capture the exact audio payload that triggered the latest incident: `/app/incident_alert.wav`.

Through manual delta debugging, we suspect the legacy algorithm fails to converge when it encounters a localized signal anomaly: specifically, continuous absolute digital silence (exact `0` amplitude samples) lasting for 50 milliseconds or more. 

Your task is to write a Python pre-filter script at `/home/user/detector.py` to protect the legacy service. 

Requirements for `/home/user/detector.py`:
1. It must take a single command-line argument: the absolute path to a WAV file.
2. It must analyze the audio data (e.g., using `scipy.io.wavfile` or `wave`).
3. If the file contains 50 consecutive milliseconds or more of exact `0` amplitude samples, it must be flagged as "unsafe" and the script must exit with a non-zero status code (e.g., `exit(1)`).
4. If the file does not contain this anomaly, it is "safe" and the script must exit with status code `0`.

To help you test your filter, we have provided two directories:
- `/app/corpus/clean/`: Contains known safe alerts.
- `/app/corpus/evil/`: Contains known unsafe alerts that trigger the convergence failure.

Your script will be tested against a hidden automated suite using the exact same criteria. It must accurately reject 100% of the evil corpus and preserve 100% of the clean corpus.