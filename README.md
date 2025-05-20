# 🧠 Proxmox Home Lab — AI-Powered Automation

Welcome to my personal home lab, built on **Proxmox VE**, with integrated tools for AI-driven insights, automated monitoring, and structured documentation. This setup merges **Obsidian**, **Grafana**, and **Python** to track system health, logs, and project metadata — with everything managed from a unified source.

---

## 🚀 Key Features

- **💡 Obsidian AI Integration** – Markdown summaries of logs, OneDrive files, and system projects.
- **📊 Grafana Dashboards** – Live panels updated with AI-generated summaries and changelogs.
- **📝 Weekly Sync Automation** – Scheduled via Task Scheduler + `.bat` helpers.
- **📁 Structured Vault** – Logs, summaries, and project notes in Obsidian’s `MainVault`.
- **⚙️ Proxmox Clustering** – 2-node setup with game and infrastructure isolation.

---

## 📁 Folder Structure

```
proxmox-homelab/
├── automation/
│   ├── grafana_helpers/
│   │   ├── sync_project_index_to_grafana.py
│   │   ├── sync_changelog_to_grafana.py
│   │   ├── update_last_sync_badge.py
│   │   ├── sync_all_to_grafana.bat
│   │   ├── last_sync_status.md
│   ├── obsidian_helpers/
│   │   ├── summarize_onedrive_files.py
│   │   ├── summarize_system_logs.py
│   │   ├── generate_project_index.py
│   │   ├── shared_config_loader.py
│   │   └── obsidian_helpers_config.json
```

---

## 🔧 How to Sync Grafana Panels

Use the `.bat` launcher to sync **everything**:

```bash
automation/grafana_helpers/sync_all_to_grafana.bat
```

It will:
- Push the latest project index to 🧠 Panel 105
- Push the changelog to 📝 Panel 102
- Update your sync badge and push it to GitHub

---

## 🧪 System Overview

| Node        | Role           | RAM     | Disk       | IP              |
|-------------|----------------|---------|------------|-----------------|
| LAB-NODE-01 | Infrastructure | 62 GB   | 1 TB NVMe  | `192.168.10.100` |
| GAME-NODE-01| Game Server    | 31 GB   | 480 GB NVMe| `192.168.10.200` |

---

## 📊 Sync Status

[![](automation/grafana_helpers/last_sync_status.md)](automation/grafana_helpers/last_sync_status.md)

---

## 📚 Project Notes

All AI-generated notes and markdown live in:
```
C:\\Users\\Steve\\Documents\\ObsidianVaults\\MainVault\\
```

Use Obsidian to explore:
- `Projects/` for indexed summaries
- `Changelog/` for synced updates
- `SystemLogs/` for log summaries

---

## 🤖 AI-Powered by

- **Ollama** – Local LLaMA3 models for markdown summarization
- **Python 3.11** – Clean helper scripts with shared config
- **Grafana + InfluxDB** – Live dashboards with text + metric panels

---

## ☁️ Hosted At

- Domain: [`stevenjvik.tech`](https://stevenjvik.tech)
- GitHub: [`UnknownOneTwo/proxmox-homelab`](https://github.com/UnknownOneTwo/proxmox-homelab)

---

> Built with ❤️ by Steven Vik — Gemini, gamer, and geek 🧠