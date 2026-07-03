apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest numpy scipy

mkdir -p /app
mkdir -p /home/user

# Generate a 60-second dummy WAV file
python3 -c '
import numpy as np
from scipy.io import wavfile

sr = 22050
duration = 60
t = np.linspace(0, duration, int(sr * duration), False)
# Generate a mix of sine waves and noise
audio = np.sin(2 * np.pi * 440 * t) + np.random.normal(0, 0.5, len(t))
# Normalize to 16-bit range
audio_int16 = np.int16(audio / np.max(np.abs(audio)) * 32767)
wavfile.write("/app/recording.wav", sr, audio_int16)
'

# Create the starter script with data leakage
cat << 'EOF' > /home/user/pipeline.py
import numpy as np
import librosa
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load audio
y, sr = librosa.load("/app/recording.wav", sr=22050)
chunk_samples = sr * 1
n_chunks = len(y) // chunk_samples

X_list = []
y_labels = []

for i in range(n_chunks):
    chunk = y[i*chunk_samples : (i+1)*chunk_samples]
    S = np.abs(librosa.stft(chunk))
    X_list.append(S.flatten())
    y_labels.append(1 if np.sum(S) > 500 else 0)

X = np.array(X_list)
y_target = np.array(y_labels)

# DATA LEAKAGE HERE:
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=10)
X_pca = pca.fit_transform(X_scaled)

X_train, X_test, y_train, y_test = train_test_split(X_pca, y_target, test_size=0.25, random_state=42)

clf = SVC(kernel='rbf', C=1.0)
clf.fit(X_train, y_train)

preds = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app