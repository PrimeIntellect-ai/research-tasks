I am a researcher running 1D hydrodynamical simulations, and I need your help filtering my simulation outputs. My pipeline recently experienced numerical instabilities, meaning many of the resulting HDF5 files contain unphysical artifacts. 

I need you to write a Python command-line tool that acts as a classifier/filter to detect these numerical instabilities. 

Here are the requirements for your script:
1. It must be written to `/home/user/classifier.py`.
2. It must accept exactly one argument: the path to an HDF5 file. (e.g., `python3 /home/user/classifier.py /path/to/data.h5`)
3. It must read the 1D array stored in the HDF5 dataset named `density`.
4. It should exit with status code `0` if the simulation is "clean" (numerically stable), and status code `1` if the simulation is "evil" (unstable).

A simulation is defined as "evil" (unstable) if EITHER of the following is true:
- The `density` array contains any `NaN` or `Inf` values.
- The absolute difference between *any* two adjacent points in the 1D `density` mesh exceeds a specific gradient threshold. 

I have forgotten the exact critical gradient threshold for this batch of simulations, but I saved a snippet of my handwritten lab notes as an image at `/app/threshold_note.png`. You will need to use OCR (e.g., the `tesseract` command line tool is installed) to read this image and extract the numerical value for the "Gradient threshold". Hardcode this exact extracted value into your Python script.

To help you develop and test your script, I have provided two corpora of HDF5 files:
- `/app/simulations/clean/`: Contains strictly stable simulation outputs.
- `/app/simulations/evil/`: Contains only unstable simulation outputs.

Your `classifier.py` must achieve 100% accuracy: it must exit `0` for every single file in the `clean` directory, and exit `1` for every single file in the `evil` directory.