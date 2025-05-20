
@echo off
setlocal
set SCRIPT=proxmox_tag_note_generator.py
set SRC=%~dp0%SCRIPT%
set NODE1=192.168.10.100
set NODE2=192.168.10.200

echo ≡ƒöü Auto-syncing %SCRIPT% to both nodes...

if not exist "%SRC%" (
    echo ❌ Script not found: %SRC%
    pause
    exit /b 1
)

scp "%SRC%" root@%NODE1%:/root/
scp "%SRC%" root@%NODE2%:/root/

echo ✅ Upload complete!
pause
