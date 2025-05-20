
@echo off
setlocal

set NODE1=192.168.10.100
set NODE2=192.168.10.200
set REMOTE_SCRIPT=/root/proxmox_tag_note_generator.py
set REMOTE_CSV=/root/lab-tag-history/latest.csv
set LOCAL_CSV_DIR=%~dp0latest_csvs
if not exist "%LOCAL_CSV_DIR%" mkdir "%LOCAL_CSV_DIR%"

echo ≡ƒöü Running tag generator on both nodes...
ssh root@%NODE1% "python3 %REMOTE_SCRIPT%"
ssh root@%NODE2% "python3 %REMOTE_SCRIPT%"

echo ≡ƒºá Downloading latest.csv from both nodes...
scp root@%NODE1%:%REMOTE_CSV% "%LOCAL_CSV_DIR%\latest-lab.csv"
scp root@%NODE2%:%REMOTE_CSV% "%LOCAL_CSV_DIR%\latest-game.csv"

echo ✅ Done! Files saved to %LOCAL_CSV_DIR%
pause
