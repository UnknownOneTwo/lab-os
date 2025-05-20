# 🧠 Proxmox + AI-Powered Home Lab  
Self-healing, AI-enhanced infrastructure using Proxmox VE, RTX 3080, and local LLMs

---

## 🔧 Project Summary

This project integrates **Proxmox VE**, **Docker**, **Grafana**, and a local **Ollama (LLaMA3)** model to build an automated, AI-supported home lab. The goal: a **resilient, modular, and insightful system** for managing infrastructure, game servers, backups, and telemetry — with natural language tools and version tracking.

---

## 🖥️ Cluster Overview

| Node         | Role         | IP              | Specs                               | Services                          |
|--------------|--------------|------------------|--------------------------------------|-----------------------------------|
| node-core-01  | Infra Core   | 192.168.10.100  | HP EliteDesk 800 G3, 62GB RAM, 1TB NVMe | InfluxDB, Grafana, Ubuntu VM      |
| node-game-01 | Game Servers | 192.168.10.200  | HP EliteDesk 800 G3, 31GB RAM, 480GB NVMe | Docker, Minecraft, Pterodactyl    |
| RTX PC       | AI Inference | 192.168.10.xxx  | RTX 3080, Windows 11                 | Ollama + LLaMA3                   |

---

## 🤖 AI Integration

### ✅ Completed Scripts
| Script                           | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `proxmox_helper_ai_backups.sh`  | Summarizes LXC/VM backup info via AI                                        |
| `proxmox_helper_ai_vmstatus.sh` | Describes system status in natural language                                 |
| `proxmox_helper_ai_resources.sh`| Reports live RAM/CPU/disk usage                                             |
| `proxmox_tag_note_generator.py` | Tags Proxmox VMs/CTs using AI + stores results to CSV                       |

### 🧪 Features in Progress
- `--log` / `--note` / `--debug` flags for all scripts
- Cached responses for faster CLI performance
- GitHub changelog integration
- Future scripts to be developed in alphabetical order

---

## 📊 Grafana Dashboard

### ✅ Integrated with InfluxDB
- Real-time monitoring for:
  - 🔥 CPU
  - 🧠 RAM
  - 💽 Disk
  - 🌡️ Temps
  - 📡 Network

### 📝 Changelog Panel
- Title: `📝 Changelog`
- CLI updatable: version, timestamp, and optional notes
- Append-only `changelog.txt` file (local)
- Future: Push changelog data to GitHub automatically

---

## 🗃️ Minecraft Game Server

### ATM10 Server (Neoforge, 470+ mods)
| Aspect         | Detail                                                                 |
|----------------|------------------------------------------------------------------------|
| Deployment     | Docker container (preferred) or Pterodactyl                            |
| Node           | node-game-01                                                           |
| ZIP Uploaded   | `ServerFiles-2.47.zip`                                                 |
| Notes          | High RAM needs (8–12GB+), mod-heavy, shaders/quests enabled            |

---

## ❌ Deprecated or Paused

### 📁 Document Tagging Project (OneDrive)
- Used Ollama to tag `.pdf` / `.docx` files
- Results saved to `file_index_with_tags.csv`
- Outcome: Script for file moving failed repeatedly, phase paused

---

## 📚 Tools and Preferences

| Tool              | Notes                                                                 |
|-------------------|-----------------------------------------------------------------------|
| Ollama (LLaMA3)   | Local LLM for summaries and tagging                                   |
| SecureCRT         | Secure terminal access to Proxmox nodes                              |
| WinSCP            | File transfer utility (Windows)                                       |
| GitHub            | Versioning, logs, changelogs                                          |
| Proxmox Scripts   | Based on best practices from [ProxmoxVE Community Scripts](https://community-scripts.github.io/ProxmoxVE/) |

---

## 🧪 Development Philosophy

- ✅ *Rebuild from scratch if stuck*
- ✅ *Step-by-step verification*
- ✅ *Scripts must log and self-describe*
- ⚠️ *GUI optional, CLI prioritized*
- ❌ *Avoid hardcoded values or AI hallucination risk*

---

## 📦 File Structure (WIP)

