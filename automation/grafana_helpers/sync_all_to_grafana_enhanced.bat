@echo off
REM === Unified Grafana Sync + Badge Update + Git Push ===

echo Syncing project index...
C:\Users\Steve\AppData\Local\Programs\Python\Python313\python.exe ^
 C:\Users\Steve\Documents\github\proxmox-homelab\automation\grafana_helpers\sync_project_index_to_grafana.py

echo Syncing changelog...
C:\Users\Steve\AppData\Local\Programs\Python\Python313\python.exe ^
 C:\Users\Steve\Documents\github\proxmox-homelab\automation\grafana_helpers\sync_changelog_to_grafana.py

echo Updating last sync badge...
C:\Users\Steve\AppData\Local\Programs\Python\Python313\python.exe ^
 C:\Users\Steve\Documents\github\proxmox-homelab\automation\grafana_helpers\update_last_sync_badge.py

echo Committing and pushing badge update to GitHub...
cd /d C:\Users\Steve\Documents\github\proxmox-homelab
git add automation\grafana_helpers\last_sync_status.md
git commit -m "📊 Auto-sync badge updated"
git push

echo ✅ All syncs complete and badge pushed to GitHub.
pause