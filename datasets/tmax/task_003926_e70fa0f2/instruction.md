As a cloud architect migrating our infrastructure to a multi-architecture environment, you need to prepare and test a localized C++ time-reporting microservice before it undergoes a rolling deployment. 

Your task is to write the C++ service, cross-compile it, and simulate a staged multi-region deployment using QEMU user-space emulation.

Complete the following steps:

1. Write a C++ program at `/home/user/tz_service.cpp` that determines its compiled architecture, reads the timezone, and determines the current system locale. 
   It must output exactly one line to standard output in this format:
   `Arch: [ARCH], TZ: [TZ_VALUE], Locale: [LOCALE_NAME]`
   - `[ARCH]` must be `AARCH64` if compiled for ARM64, and `X86_64` if compiled for x86_64 (use preprocessor macros like `__aarch64__` and `__x86_64__` to determine this).
   - `[TZ_VALUE]` must be the value of the `TZ` environment variable (if not set, output `NONE`).
   - `[LOCALE_NAME]` must be the name of the environment's default C++ locale (e.g., initialized via `std::locale("")`).

2. Compile the C++ program natively for x86_64 and output the binary to `/home/user/tz_service_x86`.

3. Cross-compile the C++ program for ARM64 using `aarch64-linux-gnu-g++` and output the binary to `/home/user/tz_service_arm`.

4. Write a deployment script at `/home/user/rolling_deploy.sh` (ensure it is executable) that simulates a rolling deployment by performing the following actions in order:
   - **Stage 1 (Tokyo Region - Native):** Execute the `/home/user/tz_service_x86` binary with the environment variables `TZ=Asia/Tokyo` and `LC_ALL=ja_JP.UTF-8`. Redirect its standard output to `/home/user/deploy_stage1.log`.
   - **Stage 2 (Berlin Region - ARM Virtualized):** Execute the `/home/user/tz_service_arm` binary using `qemu-aarch64`. You must instruct QEMU to use the appropriate shared libraries by passing the flag `-L /usr/aarch64-linux-gnu`. Run this with the environment variables `TZ=Europe/Berlin` and `LC_ALL=de_DE.UTF-8`. Redirect its standard output to `/home/user/deploy_stage2.log`.

Execute your `/home/user/rolling_deploy.sh` script to generate the logs.