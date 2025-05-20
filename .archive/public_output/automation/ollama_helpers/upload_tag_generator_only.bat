
@echo off
set NODE1=192.168.10.100
set NODE2=192.168.10.200

echo ≡ƒöü Uploading ONLY the tag generator to both nodes...

scp "%~dp0proxmox_tag_note_generator.py" root@%NODE1%:/root/
scp "%~dp0proxmox_tag_note_generator.py" root@%NODE2%:/root/

pause
