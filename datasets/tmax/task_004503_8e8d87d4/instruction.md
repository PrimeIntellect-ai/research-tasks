You are acting as a performance and scientific computing engineer. 

A colleague has left you a voice message with the parameters for a 1D heat equation simulation that has been suffering from floating-point accumulation errors due to improper reduction orders in their C++ codebase. They want you to build a clean, mathematically correct prototype to serve as the golden reference.

Your tasks:
1. Listen to / transcribe the audio file located at `/app/voicemail.wav`. It contains the exact PDE parameters: the thermal diffusivity ($\alpha$), the domain length ($L$), and the simulation end time ($T$).
2. The initial condition for the PDE is $u(x,0) = \sin(\frac{\pi x}{L})$. The boundary conditions are fixed at $0$ at both ends: $u(0,t) = u(L,t) = 0$.
3. Write a numerical PDE solver (using a language of your choice) to simulate the system from $t=0$ to $t=T$.
4. Validate your numerical solution by deriving and evaluating the exact analytical solution for this PDE. 
5. Save your final numerical results to `/home/user/pde_result.csv`. The CSV must have two columns, `x` and `u`, representing the spatial coordinates and the temperature at $t=T$. Use exactly 101 evenly spaced points for $x$ from $0$ to $L$ (inclusive).
6. Ensure your numerical approximation is highly accurate. Your solver's output will be graded programmatically by calculating the maximum absolute error against the true analytical solution.

You may install any transcription tools (like whisper or ffmpeg) and scientific libraries you need.