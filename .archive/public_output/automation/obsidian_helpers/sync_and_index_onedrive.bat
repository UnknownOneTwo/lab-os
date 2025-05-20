@echo off
echo 🌀 Running OneDrive Sync + Index for Obsidian...
cd /d C:\Users\Steve\Documents\github\proxmox-homelab

REM Run Python sync script
C:\Users\Steve\AppData\Local\Programs\Python\Python313\python.exe automation\obsidian_helpers\sync_onedrive_to_obsidian.py

REM Run index generator
C:\Users\Steve\AppData\Local\Programs\Python\Python313\python.exe automation\obsidian_helpers\generate_onedrive_index.py

echo ✅ Done! Files synced and index updated.
pause
