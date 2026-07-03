apt-get update && apt-get install -y python3 python3-pip wget ffmpeg tar
    pip3 install pytest

    mkdir -p /app/corpora/clean
    mkdir -p /app/corpora/evil

    # Create dummy wav file (doesn't need to be real audio for initial state tests)
    touch /app/machine_limits.wav

    # Create clean corpus
    for i in $(seq 1 5); do
        echo "G1 X100 Y100 Z-5" > /app/corpora/clean/clean_$i.gcode
        echo "M3 S5000" >> /app/corpora/clean/clean_$i.gcode
    done

    # Create evil corpus
    for i in $(seq 1 5); do
        echo "G1 X200 Y100 Z-5" > /app/corpora/evil/evil_$i.gcode
        echo "M3 S15000" >> /app/corpora/evil/evil_$i.gcode
    done

    # Create legacy projects
    mkdir -p /tmp/legacy/project1/subdir
    mkdir -p /tmp/legacy/project2

    echo "G1 X50 Y50 Z-2" > /tmp/legacy/project1/subdir/valid1.gcode
    echo "G1 X200 Y50 Z-2" > /tmp/legacy/project1/subdir/invalid1.gcode
    echo "dummy elf" > /tmp/legacy/project1/subdir/dummy.elf

    echo "G1 X10 Y10 Z-1" > /tmp/legacy/project2/valid2.gcode
    echo "G1 X10 Y10 Z-20" > /tmp/legacy/project2/invalid2.gcode
    echo "log data" > /tmp/legacy/project2/run.log

    cd /tmp/legacy && tar -czf /app/legacy_projects.tar.gz .
    rm -rf /tmp/legacy

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app