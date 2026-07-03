I am a researcher running a numerical simulation that integrates a system across multiple nodes using MPI and writes the final domain state to an HDF5 file using parallel I/O. 

My code is located at `/home/user/sim/integrate.c`.

Unfortunately, the simulation diverges because of a bug in the adaptive time-stepping logic. I need you to fix it and run the simulation.

Here is what you need to do:
1. Examine `/home/user/sim/integrate.c`. There is a loop that updates the step size `dt`. The logic is currently inverted: when `error > tolerance`, it multiplies `dt` by 2.0. Fix this by changing the multiplier to 0.5 so that `dt` is reduced instead.
2. The step size `dt` is calculated locally by each MPI process, but for the simulation to remain synchronized, all processes must use the exact same minimum `dt` globally. Right after the `dt` multiplier logic (and before it is used to increment `t` or `val`), insert an `MPI_Allreduce` call to compute the global minimum of `dt` across `MPI_COMM_WORLD`, and set the local `dt` to this global minimum.
3. Compile the C code using the HDF5 parallel compiler wrapper. Make sure the output executable is named `/home/user/sim/integrate`.
4. Run the executable using exactly 4 MPI processes (`mpirun -np 4 ...`).
5. The program will generate `/home/user/sim/output.h5`. Use the `h5dump` tool to read the contents of this file and save the standard output to `/home/user/result.txt`.

Please complete these steps. The test suite will verify the contents of `/home/user/result.txt` and the HDF5 file.