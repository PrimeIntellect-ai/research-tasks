You are a Machine Learning Engineer preparing a dataset of protein structures for a new predictive model. You have received a raw video from a domain-decomposed mesh simulation and a corpus of PDB (Protein Data Bank) files generated via Monte Carlo sampling. However, some of the PDB files are non-physical ("evil") and will crash the ML training pipeline. 

Your task is to write a C program that filters out these bad files based on a threshold derived from the simulation video.

Step 1: Video Analysis
You have a video file located at `/app/sim_video.mp4`. This video shows the mesh refinement process of the simulation. Most frames are completely black, but several frames are completely white. 
- Extract the frames and count the exact number of solid white frames (average pixel intensity > 250). Let this count be `W`.

Step 2: PDB Corpus Filtering
You must write a C program at `/home/user/filter_corpus.c` and compile it to `/home/user/filter_corpus`. 
Your executable must take a single argument (the path to a PDB file). 

The program must parse the PDB file and extract the 3D coordinates (x, y, z) of all `CA` (Alpha Carbon) atoms. 
- A PDB file is considered "clean" (physically valid) if the Euclidean distance between **every** pair of consecutive `CA` atoms in the file is strictly between `2.5` Angstroms and `W + 0.5` Angstroms.
- If a file violates this rule, or if it does not contain any valid `ATOM` lines for `CA`, it is considered "evil".

Your compiled C program `/home/user/filter_corpus <file_path>` must:
- Exit with code `0` if the PDB file is clean.
- Exit with a non-zero code (e.g., `1`) if the PDB file is evil.

Ensure your code handles standard PDB line formatting correctly (coordinates are in columns 31-54). Compile your program so it is ready to be tested against a hidden corpus of clean and evil files.