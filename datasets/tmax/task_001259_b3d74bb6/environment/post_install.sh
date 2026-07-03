apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy h5py emcee scipy

    mkdir -p /home/user/data
    mkdir -p /home/user/results

    cat << 'EOF' > /home/user/setup_data.py
import numpy as np
import h5py

np.random.seed(42)
N = 4000
dt = 0.02
t = np.arange(N) * dt
freq = np.fft.rfftfreq(N, d=dt)

# True spectrum parameters
B = 12.0
A = 3.5
f0 = 2.5
sigma = 0.2

# Build the amplitude spectrum
spectrum = B - A * np.exp(-0.5 * ((freq - f0) / sigma)**2)

# Add random phases to create a time-domain signal
phases = np.random.uniform(0, 2*np.pi, size=len(freq))
complex_spectrum = spectrum * np.exp(1j * phases)

# Transform to time domain
signal = np.fft.irfft(complex_spectrum, n=N)

# Add time domain noise
signal += np.random.normal(0, 0.05, size=N)

with h5py.File('/home/user/data/interferogram.h5', 'w') as f:
    f.create_dataset('time', data=t)
    f.create_dataset('signal', data=signal)
EOF

    python3 /home/user/setup_data.py
    rm /home/user/setup_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user