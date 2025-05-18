@echo off
cd /d "%~dp0\.."

:: 📝 Ask for changelog entry
set /p note=📝 Enter changelog note:

:: 🧾 Add to CHANGELOG.md
python automation\grafana_helpers\add_changelog_entry.py --note "%note%"

:: 🗃 Commit vault
echo 🔍 Committing vault changes...
git add vault
git commit -m "📦 Update Obsidian vault contents (%DATE%)"
git push origin main

:: 📡 Sync to Grafana
echo 📡 Syncing changelog to Grafana...
python automation\grafana_helpers\grafana_changelog_updater.py

echo ✅ All done! Vault committed + changelog synced.
pause
