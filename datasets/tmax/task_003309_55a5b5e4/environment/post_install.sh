apt-get update && apt-get install -y python3 python3-pip libsndfile1
    pip3 install pytest numpy scipy pandas scikit-learn librosa soundfile

    mkdir -p /app

    cat << 'EOF' > /tmp/generate_data.py
import numpy as np
from scipy.io import wavfile
import pandas as pd

def generate_data(duration_sec, num_segments, audio_path, labels_path, truth_path=None, test_segments_path=None):
    sr = 16000
    total_samples = duration_sec * sr
    np.random.seed(42 if truth_path is None else 24)
    audio = np.random.normal(0, 0.05, total_samples)

    segment_duration = 1.0
    segment_samples = int(segment_duration * sr)

    possible_starts = np.arange(0, duration_sec - segment_duration, segment_duration)
    chosen_starts = np.random.choice(possible_starts, num_segments, replace=False)
    chosen_starts.sort()

    segments = []
    for start in chosen_starts:
        label = np.random.randint(0, 2)
        start_sample = int(start * sr)
        end_sample = start_sample + segment_samples

        if label == 1:
            t = np.linspace(0, segment_duration, segment_samples, False)
            sine = 0.5 * np.sin(2 * np.pi * 440 * t)
            audio[start_sample:end_sample] += sine

        segments.append((start, start + segment_duration, label))

    audio = np.clip(audio, -1.0, 1.0)
    wavfile.write(audio_path, sr, (audio * 32767).astype(np.int16))

    df = pd.DataFrame(segments, columns=['start_time', 'end_time', 'label'])
    if truth_path is None:
        df.to_csv(labels_path, index=False)
    else:
        df[['start_time', 'end_time']].to_csv(test_segments_path, index=False)
        pd.Series(df['label']).to_csv(truth_path, index=False, header=False)

generate_data(300, 100, '/app/train_audio.wav', '/app/train_labels.csv')
generate_data(120, 40, '/app/hidden_test.wav', '', '/app/hidden_truth.csv', '/app/test_segments.csv')
EOF

    python3 /tmp/generate_data.py
    rm /tmp/generate_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app