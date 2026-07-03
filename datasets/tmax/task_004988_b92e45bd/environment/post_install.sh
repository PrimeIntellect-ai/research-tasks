apt-get update && apt-get install -y python3 python3-pip ffmpeg espeak libhdf5-dev
    pip3 install pytest h5py numpy scipy

    mkdir -p /app

    # Generate audio file
    espeak -w /app/lab_notes.wav "Please process the PDB file. Extract the alpha carbon atoms of chain B. Compute the 3D kernel density estimation using a Gaussian kernel with a bandwidth of 2.5 Angstroms. Create a 50 by 50 by 50 grid spanning from exactly -20.0 to 30.0 in the X, Y, and Z dimensions. Save the output to an HDF5 file with the dataset name 'electron_density'."

    # Generate PDB file
    cat << 'EOF' > /app/target_complex.pdb
ATOM      1  N   ALA A   1      -15.000  10.000   5.000  1.00  0.00           N
ATOM      2  CA  ALA A   1      -14.000  10.000   5.000  1.00  0.00           C
ATOM      3  C   ALA A   1      -13.000  10.000   5.000  1.00  0.00           C
ATOM      4  O   ALA A   1      -13.000  11.000   5.000  1.00  0.00           O
ATOM      5  N   ALA B   1      -15.000  10.000   5.000  1.00  0.00           N
ATOM      6  CA  ALA B   1      -14.000  10.000   5.000  1.00  0.00           C
ATOM      7  C   ALA B   1      -13.000  10.000   5.000  1.00  0.00           C
ATOM      8  O   ALA B   1      -13.000  11.000   5.000  1.00  0.00           O
ATOM      9  N   GLY B   2      -12.000   9.000   5.000  1.00  0.00           N
ATOM     10  CA  GLY B   2      -11.000   9.000   5.000  1.00  0.00           C
ATOM     11  C   GLY B   2      -10.000   9.000   5.000  1.00  0.00           C
ATOM     12  O   GLY B   2      -10.000   8.000   5.000  1.00  0.00           O
EOF

    # Generate reference HDF5 file
    cat << 'EOF' > /tmp/gen_ref.py
import numpy as np
import h5py

coords = np.array([[-14.0, 10.0, 5.0], [-11.0, 9.0, 5.0]])
N = len(coords)
h = 2.5

x = np.linspace(-20.0, 30.0, 50)
y = np.linspace(-20.0, 30.0, 50)
z = np.linspace(-20.0, 30.0, 50)

X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
grid_coords = np.vstack([X.ravel(), Y.ravel(), Z.ravel()]).T

density = np.zeros(grid_coords.shape[0])
for c in coords:
    d2 = np.sum((grid_coords - c)**2, axis=1)
    density += np.exp(-d2 / (2 * h**2))

density /= (N * (h**3) * (2*np.pi)**1.5)
density = density.reshape((50, 50, 50))

with h5py.File('/app/reference_density.h5', 'w') as f:
    f.create_dataset('electron_density', data=density, dtype='float64')
EOF
    python3 /tmp/gen_ref.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user