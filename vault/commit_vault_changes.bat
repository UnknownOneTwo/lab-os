@echo off
cd /d "%~dp0\.."
echo 🔍 Checking for changes in the vault...

git add vault
git commit -m "📦 Update Obsidian vault contents (%DATE%)"
git push origin main

echo 📡 Syncing changelog to Grafana...
python automation\grafana_helpers\grafana_changelog_updater.py

echo ✅ Vault committed and changelog pushed.
pause
