
@echo off
setlocal

echo ≡ƒöü Step 1: Syncing latest tag generator script to both nodes...
call "%~dp0auto_sync_tag_script.bat"

echo ≡ƒºá Step 2: Running tag generator and downloading logs...
call "%~dp0run_tag_generator_on_nodes.bat"

echo ✅ All tasks completed.
pause
