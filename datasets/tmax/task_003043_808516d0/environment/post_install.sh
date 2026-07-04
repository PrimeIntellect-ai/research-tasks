apt-get update && apt-get install -y python3 python3-pip cmake build-essential espeak
    pip3 install pytest

    # Create directories
    mkdir -p /home/user/emulator_project/lib
    mkdir -p /app

    # Create dummy shared library
    cat << 'EOF' > /home/user/emulator_project/lib/vmlog.c
#include <stdio.h>
void vm_log(const char* msg) {
    // dummy function
}
EOF
    gcc -shared -fPIC -o /home/user/emulator_project/lib/libvmlog.so /home/user/emulator_project/lib/vmlog.c
    rm /home/user/emulator_project/lib/vmlog.c

    # Create CMakeLists.txt
    cat << 'EOF' > /home/user/emulator_project/CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(vm_emulator)
add_executable(vm_emulator main.c vm.c)
target_link_libraries(vm_emulator vmlog)
EOF

    # Create main.c
    cat << 'EOF' > /home/user/emulator_project/main.c
#include <stdio.h>

extern void vm_execute(const char* input);

int main(int argc, char** argv) {
    if (argc != 2) return 1;
    vm_execute(argv[1]);
    return 0;
}
EOF

    # Create stub vm.c
    cat << 'EOF' > /home/user/emulator_project/vm.c
#include <stdio.h>

void vm_execute(const char* input) {
    // TODO: Implement emulator logic here
}
EOF

    # Create reference emulator
    cat << 'EOF' > /app/ref.c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    uint8_t acc = 0;
    char *p = argv[1];
    while (*p) {
        char c = *p;
        if (c >= 'A' && c <= 'Z') {
            acc += c;
        } else if (c >= '0' && c <= '9') {
            acc *= (c - '0');
        } else if (c >= 'a' && c <= 'z') {
            acc ^= c;
        } else {
            acc -= 1;
        }
        p++;
    }
    printf("%02X\n", acc);
    return 0;
}
EOF
    gcc -o /app/reference_emulator /app/ref.c
    rm /app/ref.c

    # Generate spec_memo.wav using espeak
    espeak -w /app/spec_memo.wav "Here is the specification for the virtual machine. The machine state consists of a single accumulator, initialized to zero. It is an 8-bit unsigned integer. The input is processed character by character. For each character read: If the character is an uppercase letter A through Z, add its ASCII value to the accumulator. If the character is a digit 0 through 9, multiply the accumulator by the numeric value of the digit, keeping the lower 8 bits. If the character is a lowercase letter a through z, perform a bitwise XOR of the accumulator with the character's ASCII value. For any other character, subtract 1 from the accumulator. All operations must strictly wrap around using 8-bit unsigned arithmetic. After processing all characters in the string, output the final accumulator value as a two-digit uppercase hexadecimal string, without any prefix."

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user