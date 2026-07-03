Hello, I am a bioinformatics researcher running large-scale structural simulations, and I am running into a few critical pipeline failures. I need your help to fix them. 

First, I need to extract some simulation parameters from my PI's notes. I have a scan of the lab notebook at `/app/params_notes.png`. Please use OCR (e.g., `tesseract`, which is installed) to read this image. It contains two critical values:
1. `CLASH_CUTOFF`: A distance in Angstroms.
2. `TARGET_EPSILON`: A floating-point convergence tolerance.

Second, my simulation pipeline is failing due to poisoned/corrupted PDB files scraped from a public database. I need you to create a Python script at `/home/user/filter_pdbs.py`. This script must act as a strict sanitiser. 
- Signature: `python /home/user/filter_pdbs.py <input_dir> <output_dir>`
- It must read all `.pdb` files in `<input_dir>`. 
- It should REJECT files that have structural anomalies (specifically, any two atoms with a Euclidean distance strictly less than the `CLASH_CUTOFF` extracted from the image) or invalid formatting (e.g. NaN coordinates, missing C-alpha atoms for amino acid residues).
- It should ACCEPT valid files by copying them unchanged to `<output_dir>`.

Third, the downstream calculation script at `/home/user/calc_com.py` is failing our convergence tests. It calculates the center of mass (COM) of a PDB structure. To simulate memory-mapped multi-threading, the script currently shuffles the order of atoms before accumulating their coordinates. Due to floating-point reduction order, the final COM varies slightly between runs on the same file!
- You must rewrite the accumulation logic in `/home/user/calc_com.py` so that the result is strictly deterministic and perfectly reproducible, regardless of the order in which the atoms are processed. 
- The maximum variance across 100 shuffled runs must be exactly 0.0 (or well below `TARGET_EPSILON`). 
- Make sure to use stable summation techniques (like Kahan summation or Python's built-in stable maths functions).
- The script should take a single PDB file as an argument and print the X, Y, Z coordinates to stdout, comma-separated: `python /home/user/calc_com.py sample.pdb`.

Please set up a Python virtual environment at `/home/user/venv` and install any necessary packages (e.g., `biopython`, `numpy`, `Pillow`, `pytesseract`) to complete these tasks. 

Ensure your `filter_pdbs.py` and `calc_com.py` are robust. We will test your filter against a hidden dataset of perfectly clean and heavily corrupted PDBs.