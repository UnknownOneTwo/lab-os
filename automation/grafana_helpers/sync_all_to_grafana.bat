@echo off
REM === Unified Grafana Sync ===

echo Syncing project index...
C:\Users\Steve\AppData\Local\Programs\Python\Python313\python.exe ^
 C:\Users\Steve\Documents\github\proxmox-homelab\automation\grafana_helpers\sync_project_index_to_grafana.py

echo Syncing changelog...
C:\Users\Steve\AppData\Local\Programs\Python\Python313\python.exe ^
 C:\Users\Steve\Documents\github\proxmox-homelab\automation\grafana_helpers\sync_changelog_to_grafana.py

echo ✅ Both Grafana panels synced.
pause