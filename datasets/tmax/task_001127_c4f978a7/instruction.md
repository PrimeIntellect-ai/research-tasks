You are an algorithmic script developer working on a new utility for a robotic assembly line. 

Your task is to build a custom bytecode emulator in Python that reads jobs and dependencies, merges them with a set of base constraints extracted from a video artefact, and outputs the exact execution order.

**Part 1: Video Constraint Extraction**
A visual diagnostic dump from the legacy system is provided at `/app/protocol_dump.mp4`. The video is exactly 10 seconds long at 1 frame per second (10 frames total). 
Each frame consists of a solid background color. It is entirely grayscale. 
* The grayscale intensity (0-255) of the top half of the frame represents a job ID `U`.
* The grayscale intensity (0-255) of the bottom half of the frame represents a job ID `V`.
* Each frame defines a base dependency rule: Job `U` MUST be executed before Job `V`.
Extract these 10 base dependency rules. (Assume standard rounding to the nearest integer for the grayscale values).

**Part 2: Protobuf Definition**
Create a protobuf file at `/home/user/job.proto` with the following exact definition:
```protobuf
syntax = "proto3";

message Instruction {
    enum OpType { ADD_JOB = 0; ADD_DEP = 1; EXECUTE = 2; }
    OpType op = 1;
    int32 u = 2;  // Used for ADD_JOB (job u) and ADD_DEP (u -> v)
    int32 v = 3;  // Used for ADD_DEP (u -> v)
}

message Program {
    repeated Instruction instructions = 1;
}
```
Compile this protobuf for Python to generate the necessary bindings.

**Part 3: The Emulator**
Write a Python script at `/home/user/emulator.py`. This script will be executed with a single command-line argument: the path to a binary protobuf file containing a `Program` message.

The emulator must maintain:
1. A global directed acyclic graph (DAG) of dependencies. Initialize this graph with the 10 base dependencies extracted from the video.
2. A set of "executed" jobs (initially empty).
3. A set of "pending" jobs (initially empty).
4. An "execution log" (an ordered list of executed job IDs).

Process each instruction sequentially:
* `ADD_JOB`: Add job `u` to the pending set.
* `ADD_DEP`: Add a dynamic dependency rule: `u` must be executed before `v`. Add this to your dependency graph.
* `EXECUTE`: Evaluate all jobs currently in the "pending" set. A pending job is "ready" if ALL of its dependencies (both base and dynamic) have already been placed in the "executed" set. 
  - Find all "ready" jobs.
  - Sort them by job ID in ascending order.
  - Remove them from the pending set, add them to the executed set, and append them to the execution log in that sorted order.
  - *Note: Only perform one pass of execution per `EXECUTE` instruction. Do not cascade executions.*

After all instructions are processed, print the execution log as a single comma-separated string to `stdout` (e.g., `5,12,3,9`). If the log is empty, print nothing but a newline.

Make sure your script is executable and robust. An automated testing system will verify your emulator by feeding it thousands of randomly generated protobuf files and comparing the stdout against a reference oracle.