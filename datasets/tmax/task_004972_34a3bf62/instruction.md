You are acting as a DevOps engineer investigating a crashing legacy telemetry processing service. We recently received an automated alert that our audio telemetry processing pipeline is failing and producing garbage logs. 

An audio artefact containing the most recent telemetry burst has been captured at `/app/corrupted_telemetry.wav`. This file is known to have some corrupted frames (invalid NaN values injected by a faulty sensor) which is crashing our processing binary.

The source code for the processor is located at `/home/user/telemetry_processor.c`. 
Your task is to:
1. Trace the execution of the compiled binary (which you must compile from the source) to determine exactly where and why it fails when processing `/app/corrupted_telemetry.wav`. 
2. Fix the corrupted input handling in the C code so that invalid frames (NaNs or infinites) are replaced with `0.0` instead of crashing the program or propagating NaN poisoning.
3. Fix a severe floating-point precision bug in the core filtering loop. The original developer used single-precision `float` for an accumulator in a recursive IIR filter, which diverges rapidly. You must upgrade the accumulator and relevant filter coefficients to use double-precision `double` math to prevent the signal from distorting.
4. Recompile the fixed source code and run it against `/app/corrupted_telemetry.wav`.

The program takes two arguments: the input WAV file and the output WAV file.
Command signature: `./telemetry_processor <input.wav> <output.wav>`

Your final objective is to produce the successfully processed audio file at `/home/user/clean_telemetry.wav`. 

To verify your work, we will calculate the Mean Squared Error (MSE) between the raw audio samples of your `/home/user/clean_telemetry.wav` and our known-good reference signal. You must achieve an MSE of less than 0.001. Ensure your output file is a valid 16-bit PCM WAV file matching the input sample rate.