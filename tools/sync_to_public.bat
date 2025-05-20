@echo off
setlocal EnableDelayedExpansion

:: Paths
set "PRIVATE_REPO=C:\Users\Steve\Documents\github\proxmox-homelab"
set "PUBLIC_REPO=C:\Users\Steve\Documents\github\homelab-automation-kit"
set "OUTPUT_DIR=%PRIVATE_REPO%\public_output"
set "LOGFILE=%PRIVATE_REPO%\sync_log.txt"

:: Timestamp
for /f "tokens=1-4 delims=/ " %%a in ("%date%") do set "TODAY=%%d-%%b-%%c"
for /f "tokens=1-2 delims=: " %%a in ("%time%") do set "NOW=%%a-%%b"
set "STAMP=[%TODAY% %NOW%]"

:: Log start
echo %STAMP% 🕒 Starting public sync >> "%LOGFILE%"
echo. >> "%LOGFILE%"

:: Step 1: Run sanitization
echo ≡ƒº╣ Running sanitize_for_public.py...
cd /d "%PRIVATE_REPO%"
python sanitize_for_public.py >> "%LOGFILE%" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Sanitization failed. >> "%LOGFILE%"
    echo ❌ Sanitization failed. Exiting.
    pause
    exit /b 1
)
echo ✅ Sanitization complete. >> "%LOGFILE%"

:: Step 2: Copy sanitized files
echo ≡ƒÜÜ Copying sanitized files to public repo...
robocopy "%OUTPUT_DIR%" "%PUBLIC_REPO%" /MIR /XD .git >> "%LOGFILE%" 2>&1

:: Step 3: Git commit + push
echo ≡ƒôª Committing and pushing to GitHub...
cd /d "%PUBLIC_REPO%"
git add . >> "%LOGFILE%" 2>&1
git commit -m "🔄 Auto-sync from private repo [%STAMP%]" >> "%LOGFILE%" 2>&1
git push >> "%LOGFILE%" 2>&1

:: Optional: Touch file to trigger GitHub Actions
echo 🔁 Trigger file updated on %DATE% at %TIME% > "%PUBLIC_REPO%\last_sync.txt"
git add last_sync.txt >> "%LOGFILE%" 2>&1
git commit -m "✅ Trigger GitHub Actions: %STAMP%" >> "%LOGFILE%" 2>&1
git push >> "%LOGFILE%" 2>&1

:: Done
echo %STAMP% ✅ Sync complete >> "%LOGFILE%"
echo Γ£à Public sync complete!
pause
