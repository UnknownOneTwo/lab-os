@echo off
set NODE_IP=192.168.10.100
set REMOTE_SCRIPTS=/root/scripts
set LOCAL_FOLDER=%~dp0
set DEST_FOLDER=%USERPROFILE%\Documents\Proxmox-Tags
mkdir %DEST_FOLDER% 2>nul

echo 🔁 Uploading Proxmox Tag Generator...
scp "%LOCAL_FOLDER%proxmox_tag_note_generator.py" root@%NODE_IP%:/root/

echo 🔁 Uploading Weekly Snapshot Script...
scp "%LOCAL_FOLDER%weekly_vm_snapshots.sh" root@%NODE_IP%:%REMOTE_SCRIPTS%/

echo ⬇️ Downloading latest tag notes...
scp root@%NODE_IP%:/root/lab-tag-history/latest.csv "%DEST_FOLDER%\latest.csv"

echo ✅ All tasks completed.
pause
