@echo off
cd /d "%~dp0\.."

:: 📝 Prompt for changelog note
set /p note=📝 Enter changelog note:
set /p version=🔢 Enter version (optional, press Enter to skip):

:: 🧾 Add to CHANGELOG.md
if "%version%"=="" (
    python automation\grafana_helpers\add_changelog_entry.py --note "%note%"
) else (
    python automation\grafana_helpers\add_changelog_entry.py --note "%note%" --version %version%
)

:: 🗃 Commit vault changes
echo 🔍 Committing vault changes...
git add vault
git commit -m "📦 Update Obsidian vault contents (%DATE%)"
git push origin main

:: 📡 Sync changelog to Grafana
echo 📡 Syncing changelog to Grafana...
python automation\grafana_helpers\grafana_changelog_updater.py

echo ✅ All done! Vault committed + changelog synced.
pause
