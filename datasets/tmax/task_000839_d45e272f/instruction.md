You are assisting a materials researcher in analyzing simulation data of a composite material undergoing high-stress testing. The simulation produces high-resolution spatial mesh data, and spectroscopy readings are taken at various domain boundaries to detect structural instabilities.

Due to numerical instability in the mesh refinement process, some simulation runs produce anomalous, noisy signals. We need a filtering tool written in Go to automatically classify and reject these unstable runs based on their spectral properties.

First, you need to determine the base calibration frequency ($f_c$) of the spectrograph. The lab technician left a scan of the calibration notes at `/app/calibration_note.png`. Use an OCR tool (like `tesseract`, which is installed) to read this image and extract the value of $f_c$ (in Hz). 

Next, write a Go program at `/home/user/filter.go` that analyzes a directory of CSV files containing time-series spectroscopy data.
Each CSV file has two columns without headers: time in seconds (`t`) and signal amplitude (`v`). The sampling rate is exactly $2000 \text{ Hz}$ for all files.

Your Go program must perform the following:
1. Accept a single command-line argument: the path to a directory containing the `.csv` files.
2. Iterate through all `.csv` files in the given directory.
3. For each file, compute the Discrete Fourier Transform (DFT) of the signal to obtain its frequency spectrum.
4. Calculate the total spectral energy of the signal, defined as $E_{total} = \sum |X(k)|^2$ for all frequency bins $k$.
5. Calculate the high-frequency energy, $E_{high}$, which is the sum of $|X(k)|^2$ for all frequencies strictly greater than $1.2 \times f_c$.
6. If the ratio $E_{high} / E_{total}$ exceeds $0.15$ (15%), the signal is considered unstable (anomalous).
7. For each file, print exactly one line to standard output in the format:
   `ACCEPT filename.csv` (if stable) or `REJECT filename.csv` (if unstable).

You may use standard Go libraries or popular third-party mathematical libraries like `gonum.org/v1/gonum`. A small sample dataset is available at `/home/user/sample_data/` for you to test your logic, but your tool will be evaluated against a hidden, much larger dataset containing verified "clean" (stable) and "evil" (unstable) simulation outputs.

Ensure your program compiles and runs cleanly, as it will be invoked directly by the automated verification suite.