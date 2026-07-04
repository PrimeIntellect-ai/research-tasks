apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user

    python3 -c "
import tarfile
import os
import io

os.makedirs('/home/user', exist_ok=True)

gcode_a = b'''G28
G1 Z15.0 F6000
M109 S210 ; set temp
G92 E0
'''

gcode_b = b'''M104 S150
M109 S215
G28
M109 S220 ; higher temp for later
'''

not_gcode = b'''This is a text file.
It mentions M109 S500 but shouldn\'t be parsed.
'''

tar_path = '/home/user/prints.tar.gz'

with tarfile.open(tar_path, 'w:gz') as tar:
    info1 = tarfile.TarInfo(name='../../etc/shadow_fake.gcode')
    info1.size = len(gcode_a)
    tar.addfile(info1, io.BytesIO(gcode_a))

    info2 = tarfile.TarInfo(name='../project/subdir/part2.gcode')
    info2.size = len(gcode_b)
    tar.addfile(info2, io.BytesIO(gcode_b))

    info3 = tarfile.TarInfo(name='../../var/tmp/notes.txt')
    info3.size = len(not_gcode)
    tar.addfile(info3, io.BytesIO(not_gcode))

os.chmod(tar_path, 0o644)
"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user