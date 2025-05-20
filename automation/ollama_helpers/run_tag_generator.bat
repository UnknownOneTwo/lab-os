@echo off
setlocal

REM Define paths
set SCRIPT_NAME=proxmox_tag_note_generator.py
set NODE_IP=192.168.10.100
set REMOTE_PATH=/root/%SCRIPT_NAME%

echo 📤 Uploading %SCRIPT_NAME% to Proxmox node at %NODE_IP%...
scp %SCRIPT_NAME% root@%NODE_IP%:%REMOTE_PATH%

echo 🧠 Running script on the node...
ssh root@%NODE_IP% "python3 %REMOTE_PATH%"

echo ✅ Done! Output saved to proxmox_tag_notes.csv on the node.

pause
