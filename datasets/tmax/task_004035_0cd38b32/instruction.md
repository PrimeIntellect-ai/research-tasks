You are tasked with fixing, organizing, and building a C++ project for a custom Stack Virtual Machine (VM) emulator. 

Currently, the project is a mess. The files are all in the root directory `/home/user/stack-vm`, the CMake configuration is broken (it fails to link the shared library properly), and the VM's state serialization feature is unimplemented.

Here is what you need to do:

1. **Reorganize the Project:**
   In `/home/user/stack-vm`, organize the source files into standard directories:
   - Create `include/` and move `vm_engine.h` into it.
   - Create `src/` and move `vm_engine.cpp` and `main.cpp` into it.

2. **Patch the Serialization Logic:**
   The repository contains a patch file at `/home/user/stack-vm/serialization.patch`.
   Apply this patch to the project. It implements binary serialization and deserialization for the VM's internal stack state so that `SAVE` and `LOAD` instructions work.

3. **Fix the CMake Configuration:**
   Modify `/home/user/stack-vm/CMakeLists.txt` to account for your new directory structure. 
   Currently, the `CMakeLists.txt` is broken: it builds a shared library (`libvm_engine.so`) and an executable (`vm-cli`), but it fails to find the header files and fails to link the library to the executable. 
   Fix the CMake file so that:
   - The include directory `include/` is exposed properly to the targets.
   - The executable `vm-cli` successfully links against the shared library `vm_engine`.
   - The executable has its RPATH set appropriately (e.g., using `$ORIGIN/../lib` or standard CMake RPATH setups) so it can find the shared library at runtime without needing `LD_LIBRARY_PATH` modifications.
   - The built executable must be output to `/home/user/stack-vm/build/bin/` and the shared library to `/home/user/stack-vm/build/lib/`.

4. **Build the Project:**
   Use CMake to build the project inside the `/home/user/stack-vm/build` directory.

5. **Run the Emulator:**
   The VM reads instruction scripts. We have provided two scripts: `prog1.txt` and `prog2.txt`.
   First, run the emulator on `prog1.txt`:
   `/home/user/stack-vm/build/bin/vm-cli /home/user/stack-vm/prog1.txt`
   This will execute instructions and save the serialized VM state to `/home/user/state.bin`.
   
   Next, run the emulator on `prog2.txt`:
   `/home/user/stack-vm/build/bin/vm-cli /home/user/stack-vm/prog2.txt`
   This will load the previously saved state, perform further calculations, and write the final output to `/home/user/result.log`.

Verify your work by ensuring `/home/user/result.log` contains the correct integer result produced by the VM emulator.