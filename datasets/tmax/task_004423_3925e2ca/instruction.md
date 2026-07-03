Hello, I need you to help me fix and extend a molecular simulation service written in Go. 

Currently, our researchers are complaining about non-reproducible results. We have a Go program that calculates the total electrostatic-like potential energy of a protein by parsing a PDB file and integrating the pairwise interactions. However, the result changes slightly on every run. I suspect this is because the program stores the parsed atoms in a standard Go map and iterates over them to compute the sum. Because map iteration order is randomized in Go, the floating-point reduction (summation) happens in a different order each time, leading to non-deterministic truncation errors.

Here is what you need to do:

1. **Extract Calibration Weights**: We received a calibration image located at `/app/calibrations/weights.png`. Use standard OCR tools (like `tesseract`) to extract the calibration weights for three specific atom types: `CA` (Alpha Carbon), `C` (Carbonyl Carbon), and `N` (Amide Nitrogen). The image contains text like "CA: X.XX", "C: Y.YY", "N: Z.ZZ".

2. **Fix the Simulation Code**: 
   - You will need to write or fix the Go program to parse standard ATOM records from a PDB format.
   - For every pair of atoms $i$ and $j$ (where $i < j$ by their sequential atom serial number in the PDB), calculate the pairwise energy: `E_{ij} = (Weight_i * Weight_j) / Distance(i, j)`. 
   - If an atom type is not CA, C, or N, its weight is 1.0.
   - **Crucially**: To fix the floating-point reduction bug, you must accumulate the total energy strictly in order. Specifically, iterate $i$ from the lowest atom serial number to the highest, and for each $i$, iterate $j$ from $i+1$ to the highest serial number. Accumulate the sum sequentially into a single `float64` variable.

3. **Deploy as an HTTP Service**: 
   Instead of a CLI script, wrap this fixed simulation into an HTTP REST service written in Go.
   - Listen exactly on `127.0.0.1:8080`.
   - **Endpoint 1**: `POST /simulate`
     - Expects a raw PDB file content in the request body (text/plain).
     - Returns a JSON response: `{"energy": <float64>}` with the deterministic total energy.
   - **Endpoint 2**: `POST /compare`
     - Expects a JSON body: `{"energy_old": <float64>, "energy_new": <float64>}`.
     - Returns a JSON response: `{"significant": <boolean>}`. The value should be `true` if the absolute difference between the two energies is strictly greater than `1e-5`, and `false` otherwise. (This acts as our statistical hypothesis comparison tool for regression testing).
   - Require an Authorization header for all requests: `Authorization: Bearer sim-token-2024`. Return a 401 Unauthorized if missing or incorrect.

Build and start your Go service in the background so it is running and bound to the port when you finish. Ensure all dependencies are properly initialized in `/app/sim`.