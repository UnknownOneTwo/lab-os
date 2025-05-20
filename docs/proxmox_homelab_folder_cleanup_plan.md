# 📁 Proxmox Home Lab – Folder Cleanup & Structure Plan

This markdown defines what should stay, what should be archived, and what should be considered for visual/docs purposes.

---

## ✅ Active Folders

These are actively used in automation, synced tools, or the README:

```
automation/
├── grafana_helpers/
├── obsidian_helpers/
├── ollama_helpers/
docs/                  ← Optional for MkDocs or Obsidian docs mirror
dashboards/            ← JSON models or layout ideas
```

---

## 🗂️ Suggested Archive

Move to `.archive/` or `legacy/` folder:

```
vault/                 ← Legacy vault, replaced by ObsidianVaults/MainVault
public_output/         ← Output from sanitize scripts, not public anymore
logs/                  ← Raw outputs, can be zipped or moved
```

---

## 🧹 Misc Cleanup

| File / Folder                        | Action                 | Reason                              |
|-------------------------------------|------------------------|-------------------------------------|
| `*.bat` (not used)                  | Move to `tools/`       | Keep helpful, clean clutter         |
| `New Text Document.txt`            | Delete                 | Placeholder file                    |
| `.publicignore`                    | Keep (if used)         | Leave unless obsolete               |
| `README_proxmox_homelab.md`        | Delete                 | Already renamed to `README.md`      |

---

## 🔧 After Cleanup, Final Folder Tree

```
proxmox-homelab/
├── automation/
│   ├── grafana_helpers/
│   ├── obsidian_helpers/
│   ├── ollama_helpers/
├── dashboards/
├── docs/
├── tools/                ← scripts and utilities
├── .archive/             ← legacy files
├── README.md
```

---

Let me know if you'd like me to:
- Generate `.bat` scripts to move folders for you
- Create the `.archive/` and `tools/` structure
- Set up a minimal MkDocs config