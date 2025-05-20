@echo off
setlocal

set NODE1=192.168.10.100
set NODE2=192.168.10.200
set REMOTE_SCRIPTS=/root/scripts
set DEST_FOLDER=%USERPROFILE%\Documents\Proxmox-Tags
mkdir %DEST_FOLDER% 2>nul

echo 🔁 Uploading tag generator to both nodes...
scp "%~dp0proxmox_tag_note_generator.py" root@%NODE1%:/root/
scp "%~dp0proxmox_tag_note_generator.py" root@%NODE2%:/root/

echo 🔁 Uploading snapshot script to both nodes...
scp "%~dp0weekly_vm_snapshots.sh" root@%NODE1%:%REMOTE_SCRIPTS%/
scp "%~dp0weekly_vm_snapshots.sh" root@%NODE2%:%REMOTE_SCRIPTS%/

echo 🧠 Running tag generator on both nodes...
ssh root@%NODE1% "python3 /root/proxmox_tag_note_generator.py"
ssh root@%NODE2% "python3 /root/proxmox_tag_note_generator.py"

echo ⬇️ Downloading latest.csv from both nodes...
scp root@%NODE1%:/root/lab-tag-history/latest.csv "%DEST_FOLDER%\latest-LAB.csv"
scp root@%NODE2%:/root/lab-tag-history/latest.csv "%DEST_FOLDER%\latest-GAME.csv"

echo ✅ All node automation complete.
pause
