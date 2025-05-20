@echo off
set NODE_IP=192.168.10.100
set DEST_FOLDER=%USERPROFILE%\Documents\Proxmox-Tags
mkdir %DEST_FOLDER% 2>nul

echo ⬇️ Pulling latest.csv from Proxmox...
scp root@%NODE_IP%:/root/lab-tag-history/latest.csv %DEST_FOLDER%\latest.csv

echo ✅ Done! File saved to %DEST_FOLDER%\latest.csv
pause
